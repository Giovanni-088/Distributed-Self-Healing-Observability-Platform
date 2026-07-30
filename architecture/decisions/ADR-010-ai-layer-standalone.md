# ADR-010 — Standalone AI Layer

## Status

Accepted

## Decision

Implement the AI layer as a standalone Python service instead of integrating it through n8n.

## Rationale

- Keeps the platform self-contained.
- Removes dependency on external automation infrastructure.
- Maintains architectural consistency.
- Demonstrates direct API integration.

## Consequences

The platform remains autonomous while reducing operational dependencies.
