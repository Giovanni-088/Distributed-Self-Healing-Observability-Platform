# ADR-006: Distributed Watchdog Architecture

## Status

Accepted

## Context

The project required a decision on how the Self-Healing Engine should operate across multiple infrastructure nodes.

Two approaches were evaluated:

1. **Distributed Watchdog**
   - One watchdog instance per Docker host.
   - Each instance monitors only its local Docker Engine.

2. **Centralized Watchdog**
   - A single watchdog running on the Application Server.
   - Remote management of containers through the Docker Remote API.

## Decision

The project adopts a **distributed watchdog architecture**.

Each Docker host runs its own independent watchdog instance.

## Rationale

This approach provides several advantages:

- Aligns with the project's distributed self-healing philosophy.
- Eliminates a single point of failure.
- Avoids exposing the Docker API over the network.
- Reduces security risks associated with remote Docker socket access.
- Requires no additional configuration since the Docker SDK automatically communicates with the local Docker socket.

## Consequences

Each infrastructure node is responsible for protecting its own services.

Failures affecting one node do not impact the recovery capability of the remaining nodes.

This architecture improves resilience while keeping the deployment simple and secure.
