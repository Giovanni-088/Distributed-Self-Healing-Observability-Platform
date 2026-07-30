"""
incident_analyzer.py — Reads incident logs and generates human-readable
summaries using Groq's LLM API. Designed to run periodically (e.g. via
systemd timer) and alert on patterns worth human attention (e.g. a
container flapping repeatedly).

Usage:
    export GROQ_API_KEY="..."
    export TELEGRAM_BOT_TOKEN="..."
    export TELEGRAM_CHAT_ID="..."
    python3 incident_analyzer.py
"""
import os
import socket
import logging
from datetime import datetime, timezone, timedelta

import requests

logger = logging.getLogger("watchdog.incident_analyzer")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

HOSTNAME = socket.gethostname()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

INCIDENT_LOG = os.path.expanduser("~/Distributed-Self-Healing-Observability-Platform/watchdog/logs/incidents.log")

LOOKBACK_HOURS = int(os.getenv("ANALYZER_LOOKBACK_HOURS", "24"))
FLAP_THRESHOLD = int(os.getenv("ANALYZER_FLAP_THRESHOLD", "3"))


def read_recent_incidents() -> list[dict]:
    """Parses incidents.log and returns entries from the last LOOKBACK_HOURS."""
    if not os.path.exists(INCIDENT_LOG):
        logger.info("No incident log found at %s — nothing to analyze.", INCIDENT_LOG)
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    incidents = []

    with open(INCIDENT_LOG, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                parts = dict(p.split("=", 1) for p in line.split(" | ")[1:])
                timestamp_str = line.split(" | ")[0]
                timestamp = datetime.fromisoformat(timestamp_str)
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=timezone.utc)
                if timestamp >= cutoff:
                    incidents.append({
                        "timestamp": timestamp,
                        "container": parts.get("container", "unknown"),
                        "outcome": parts.get("outcome", "unknown"),
                        "attempts": parts.get("attempts", "0"),
                    })
            except (ValueError, IndexError) as e:
                logger.warning("Could not parse log line: %s (%s)", line, e)

    return incidents


def detect_flapping(incidents: list[dict]) -> dict:
    """Counts incidents per container to detect repeated failures (flapping)."""
    counts: dict[str, int] = {}
    for inc in incidents:
        counts[inc["container"]] = counts.get(inc["container"], 0) + 1
    return {name: count for name, count in counts.items() if count >= FLAP_THRESHOLD}


def summarize_with_groq(incidents: list[dict], flapping: dict) -> str:
    """Sends incident data to Groq and returns a human-readable summary."""
    if not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not configured, skipping AI summary.")
        return ""

    if not incidents:
        return ""

    incident_lines = "\n".join(
        f"- {inc['timestamp'].isoformat()} | {inc['container']} | {inc['outcome']} | attempts={inc['attempts']}"
        for inc in incidents
    )

    flap_lines = "\n".join(f"- {name}: {count} incidents" for name, count in flapping.items())

    prompt = f"""You are an SRE assistant summarizing container incidents for a self-healing
observability platform running on node "{HOSTNAME}".

Incidents in the last {LOOKBACK_HOURS}h:
{incident_lines}

Containers with repeated failures (flapping, >= {FLAP_THRESHOLD} incidents):
{flap_lines if flap_lines else "None"}

Write a short (max 5 sentences) plain-language summary for a Telegram message.
Mention which container(s) are most concerning and give ONE brief, practical
suggestion if there's a flapping pattern. Do not use markdown headers. Keep it casual
but professional, in Spanish."""

    try:
        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300,
                "temperature": 0.3,
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException as e:
        logger.error("Groq API request failed: %s", e)
        return ""
    except (KeyError, IndexError) as e:
        logger.error("Unexpected Groq response format: %s", e)
        return ""


def send_telegram_summary(summary: str) -> None:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured, cannot send summary.")
        return

    message = f"🧠 *Incident Analysis* [{HOSTNAME}]\n\n{summary}"

    try:
        resp = requests.post(
            TELEGRAM_URL,
            data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"},
            timeout=10,
        )
        resp.raise_for_status()
        logger.info("Summary sent to Telegram.")
    except requests.RequestException as e:
        logger.error("Failed to send summary to Telegram: %s", e)


def main() -> None:
    incidents = read_recent_incidents()
    logger.info("Found %d incidents in the last %dh.", len(incidents), LOOKBACK_HOURS)

    if not incidents:
        logger.info("Nothing to analyze, exiting.")
        return

    flapping = detect_flapping(incidents)
    if flapping:
        logger.warning("Flapping detected: %s", flapping)

    summary = summarize_with_groq(incidents, flapping)
    if summary:
        logger.info("Summary generated:\n%s", summary)
        send_telegram_summary(summary)
    else:
        logger.info("No summary generated (missing API key or no incidents).")


if __name__ == "__main__":
    main()
