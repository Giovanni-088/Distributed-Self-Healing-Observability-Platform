# ADR-006: Direct Docker SDK Polling for the Self-Healing Engine

## Status

Accepted

## Context

The initial architecture proposed an event-driven recovery pipeline based on:

Prometheus → Alertmanager → Watchdog

During implementation, a simpler approach was evaluated using direct container monitoring through the Docker SDK.

## Decision

The watchdog performs periodic health checks directly against the Docker Engine API instead of waiting for Alertmanager notifications.

## Rationale

- Lower implementation complexity.
- Fewer infrastructure dependencies.
- Faster validation of the recovery workflow.
- Suitable for a single-host self-healing implementation.

## Consequences

The current implementation prioritizes simplicity while preserving automatic detection and recovery.

Future versions may integrate Alertmanager as an event source if centralized, event-driven recovery becomes necessary across multiple infrastructure nodes.
