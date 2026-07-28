## Watchdog Architecture

The Self-Healing Engine is implemented as a modular Python application running on the Application Server.

The watchdog consists of four independent modules:

| Module | Responsibility |
|----------|----------------|
| `main.py` | Main execution loop and orchestration |
| `docker_monitor.py` | Container health monitoring through the Docker SDK |
| `recovery.py` | Automatic restart logic with retry and backoff strategy |
| `notifier.py` | Telegram notifications |

The execution flow is performed continuously at a configurable interval:

```text
Container Monitoring
        │
        ▼
Health Verification
        │
        ▼
Container Down?
        │
   Yes ───────► Telegram Alert
        │
        ▼
Automatic Recovery
        │
        ▼
Recovered?
   │             │
 Yes            No
 │               │
 ▼               ▼
Recovery Log   Failure Log
 │               │
 ▼               ▼
Telegram      Telegram
Success       Failure
```

Operational events are written to `watchdog.log`, while recovery outcomes are recorded separately in `incidents.log` using a structured format suitable for future integrations.

## Notifications

Telegram is used as the notification channel for recovery events.

Credentials are loaded exclusively from environment variables, preventing secrets from being stored inside the source code.

Three notification types are generated:

- 🔴 Container unavailable
- 🟢 Recovery successful
- ⚠️ Recovery failed after all retry attempts

If Telegram credentials are unavailable, the watchdog continues running normally and records a warning in the operational log instead of terminating. This fail-safe behavior prevents the notification system from becoming a single point of failure.

## End-to-End Validation

The recovery workflow was validated through a controlled failure scenario.

Test procedure:

1. Stop a monitored container manually.
2. Wait for the watchdog polling interval.
3. Verify automatic detection.
4. Verify Telegram notification.
5. Verify automatic restart.
6. Verify incident logging.

Observed workflow:

```text
Container stopped
        │
        ▼
Detection (<30 seconds)
        │
        ▼
Telegram notification
        │
        ▼
Automatic restart
        │
        ▼
Recovery confirmation
        │
        ▼
Incident recorded
```

The complete recovery cycle executed successfully without manual intervention, validating the primary objective of the Self-Healing Engine.

## Future Improvements

Planned enhancements include:

- Extend monitoring to additional infrastructure nodes.
- Evaluate a distributed watchdog deployment model.
- Integrate Alertmanager as an event source instead of relying exclusively on Docker SDK polling.
- Expand recovery actions beyond container restarts.
