# ADR-004: Native Binaries for the Edge Monitoring Node

## Status

Accepted

## Context

The original platform design assumed a Docker-based deployment across all three nodes. During the deployment of the edge monitoring node, the operating system was identified as Debian 12 (Bookworm) running on the i386 architecture.

Although the processor supports 64-bit execution, the installed operating system is 32-bit. Docker CE no longer provides packages for the i386 architecture, preventing a container-based deployment on this node.

## Decision

The existing operating system was preserved and Prometheus exporters were deployed as native binaries managed by systemd instead of Docker containers.

The edge node provides:

- Node Exporter
- Blackbox Exporter

Both services run under dedicated non-login users and start automatically through systemd.

## Rationale

- Existing system hardening was already completed and verified.
- The node only exposes metrics and does not require container orchestration.
- Official linux-386 binaries are provided by the Prometheus project.
- Avoids unnecessary operating system reinstallation.
- Maintains a functional and secure edge monitoring architecture.

## Consequences

The platform intentionally operates with a heterogeneous deployment model:

- Application nodes use Docker.
- Observability nodes use Docker.
- The edge monitoring node uses native binaries.
