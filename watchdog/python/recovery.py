"""
recovery.py — Attempts to recover failed containers with retries and backoff.
"""
import time
import logging
import docker

logger = logging.getLogger("watchdog.recovery")

MAX_RETRIES = 3
BACKOFF_SECONDS = 5


def attempt_restart(client: docker.DockerClient, container_name: str) -> bool:
    """
    Attempts to restart a container up to MAX_RETRIES times,
    with incremental backoff between attempts.
    Returns True if the container ended up 'running', False otherwise.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            container = client.containers.get(container_name)
            logger.info("Attempt %d/%d: restarting %s", attempt, MAX_RETRIES, container_name)
            container.restart(timeout=10)

            time.sleep(3)  # give the container time to fully come up
            container.reload()

            if container.status == "running":
                logger.info("%s recovered successfully on attempt %d", container_name, attempt)
                return True

            logger.warning("%s still in state '%s' after attempt %d", container_name, container.status, attempt)

        except docker.errors.NotFound:
            logger.error("Container %s does not exist, cannot restart", container_name)
            return False
        except docker.errors.APIError as e:
            logger.error("Docker API error while restarting %s: %s", container_name, e)

        if attempt < MAX_RETRIES:
            wait = BACKOFF_SECONDS * attempt
            logger.info("Waiting %ds before next attempt...", wait)
            time.sleep(wait)

    logger.error("%s could not recover after %d attempts", container_name, MAX_RETRIES)
    return False
