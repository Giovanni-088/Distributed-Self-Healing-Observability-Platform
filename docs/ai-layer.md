# AI Layer

## Architecture

The AI layer extends the self-healing engine by periodically analyzing recovered incidents instead of reacting in real time.

The implementation is fully self-contained and does not depend on external automation platforms.

### Workflow

1. Read `incidents.log`
2. Filter recent incidents
3. Detect recurring failures (flapping)
4. Generate an AI prompt
5. Request analysis from Groq
6. Send the summary through Telegram

If no incidents are detected, the analyzer exits without generating notifications.

---

## Incident Analyzer

The analyzer shares the same virtual environment, logging structure, and environment variables used by the watchdog.

Main responsibilities:

- Parse incident history
- Detect repeated failures
- Generate operational summaries
- Recommend possible root causes
- Reduce alert fatigue

---

## Validation

The analyzer successfully summarized real incidents generated during recovery testing.

The generated report correctly identified:

- recovered containers
- absence of flapping
- operational recommendations

The resulting analysis was delivered through Telegram using the dedicated AI notification format.

---

## Future Improvements

Potential enhancements include:

- historical trend analysis
- anomaly detection
- incident severity scoring
- maintenance recommendations
- integration with Alertmanager alerts
