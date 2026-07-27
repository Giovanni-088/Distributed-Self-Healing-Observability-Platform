# ADR-003: Container Strategy

## Status

Accepted

## Date

2026-07-27

---

# Context

The platform requires several infrastructure services:

* Nginx.
* cAdvisor.
* Node Exporter.
* Future application workloads.

These services could be installed directly on the operating system, but this approach increases dependency management complexity and reduces portability.

---

# Decision

Infrastructure services will be deployed using Docker containers instead of native operating system packages.

---

# Reasons

## Isolation

Each service runs independently from the host system and other workloads.

Benefits:

* Reduced dependency conflicts.
* Easier troubleshooting.
* Independent lifecycle management.

---

## Reproducibility

Containers allow the environment to be recreated consistently using:

* Docker Compose.
* Versioned configuration files.
* Infrastructure as Code practices.

---

## Portability

Containerized services can be migrated to another Linux host with minimal changes.

---

## Simplified Maintenance

Updates are performed by replacing container images instead of modifying system packages.

Example:

```bash
docker compose pull
docker compose up -d
```

---

# Consequences

## Positive

* Consistent deployments.
* Easier rollback process.
* Better separation between services.
* Simplified automation.

## Negative

* Additional container management layer.
* Requires Docker knowledge.
* Some services require privileged access.

---

# Applied Services

| Service       | Deployment Method |
| ------------- | ----------------- |
| Nginx         | Docker Container  |
| cAdvisor      | Docker Container  |
| Node Exporter | Docker Container  |

---

# Future Considerations

All future application services should prioritize container deployment unless there is a specific operational reason to use native installation.
