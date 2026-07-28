"""
notifier.py — Sends watchdog alerts to Telegram.
"""
import os
import logging
import requests

logger = logging.getLogger("watchdog.notifier")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


def send_alert(message: str) -> bool:
    """Send a message to Telegram. Returns True if sent successfully."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured (missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID). Message: %s", message)
        return False

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        resp = requests.post(API_URL, data=payload, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error("Failed to send Telegram alert: %s", e)
        return False


def notify_container_down(container_name: str) -> None:
    send_alert(f"🔴 *Container down*\n`{container_name}` is not running.")


def notify_recovery_success(container_name: str) -> None:
    send_alert(f"🟢 *Recovery successful*\n`{container_name}` was restarted and is active again.")


def notify_recovery_failed(container_name: str, attempts: int) -> None:
    send_alert(
        f"⚠️ *Recovery failed*\n`{container_name}` could not recover after {attempts} attempts. "
        f"Manual intervention required."
    )
