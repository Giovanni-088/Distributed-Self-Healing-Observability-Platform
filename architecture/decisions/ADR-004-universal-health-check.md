# ADR-004: Universal Health Check Strategy

## Status

Accepted

## Date

2026-07-27

---

# Context

The infrastructure contains multiple nodes with different responsibilities:

- Application Server.
- Observability Server.
- Edge Monitoring Node.

Initially, each server required its own health-check script because every node exposed different services and ports.

This approach created configuration drift and synchronization problems.

---

# Problem

Maintaining separate scripts caused:

- Different versions between servers.
- Manual modifications.
- Risk of overwriting changes during Git synchronization.

---

# Decision

Implement a single universal health-check script shared by all nodes.

Location:

```text
scripts/health-check.sh
```

# Implementation

The script dynamically detects:

Active Docker containers.
Published ports.
Service-specific health endpoints.

Health validation is performed according to the detected service.


#Benefits

## Consistency

All nodes use the same validation logic.

## Maintainability

Changes are implemented once instead of replicated across multiple servers.

## Scalability

New services can be added by extending the health endpoint mapping.

# Future Improvements

Possible enhancements:

- Configuration files per node role.
- Automatic exporter detection.
- Integration with Alertmanager.
- Automatic remediation triggers.

---
