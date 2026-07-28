"""
main.py — Main watchdog loop: monitors containers, triggers automatic
recovery, and notifies on incidents.

Usage:
    export TELEGRAM_BOT_TOKEN="..."
    export TELEGRAM_CHAT_ID="..."
    python3 main.py
"""
import os
import time
import logging
from datetime import datetime

import docker_monitor
import recovery
import notifier

CHECK_INTERVAL_SECONDS = int(os.getenv("WATCHDOG_INTERVAL", "30"))

MONITORED_CONTAINERS = [
    "nginx",
    "cadvisor",
    "node-exporter",
]

LOG_DIR = os.path.expanduser("~/Distributed-Self-Healing-Observability-Platform/watchdog/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "watchdog.log")
INCIDENT_LOG = os.path.join(LOG_DIR, "incidents.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("watchdog.main")


def log_incident(container_name: str, outcome: str, attempts: int = 0) -> None:
    """Logs an incident to a dedicated file, separate from the general log."""
    timestamp = datetime.utcnow().isoformat()
    with open(INCIDENT_LOG, "a") as f:
        f.write(f"{timestamp} | container={container_name} | outcome={outcome} | attempts={attempts}\n")


def monitor_loop() -> None:
    client = docker_monitor.get_client()
    logger.info("Watchdog started. Monitoring: %s", ", ".join(MONITORED_CONTAINERS))
    logger.info("Check interval: %ds", CHECK_INTERVAL_SECONDS)

    while True:
        for container_name in MONITORED_CONTAINERS:
            healthy = docker_monitor.is_healthy(client, container_name)

            if healthy:
                logger.debug("%s: OK", container_name)
                continue

            status = docker_monitor.check_container_status(client, container_name)

            if status is None:
                logger.error("%s does not exist — skipping, needs manual review", container_name)
                continue

            logger.warning("%s is not healthy (status: %s). Starting recovery...", container_name, status)
            notifier.notify_container_down(container_name)

            recovered = recovery.attempt_restart(client, container_name)

            if recovered:
                notifier.notify_recovery_success(container_name)
                log_incident(container_name, "recovered", recovery.MAX_RETRIES)
            else:
                notifier.notify_recovery_failed(container_name, recovery.MAX_RETRIES)
                log_incident(container_name, "failed", recovery.MAX_RETRIES)

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logger.info("Watchdog stopped manually.")
    except Exception as e:
        logger.critical("Watchdog crashed: %s", e, exc_info=True)
        raise
