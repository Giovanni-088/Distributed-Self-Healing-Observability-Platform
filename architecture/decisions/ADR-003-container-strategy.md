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

# Docker Network Strategy Decision

## Context

A custom Docker network was initially considered to allow services to communicate using container names.

Example:

grafana → prometheus
grafana → loki

However, connecting running containers to an additional Docker network using:

docker network connect

caused routing changes inside containers.

The additional network modified the default route, affecting outbound connectivity from containers to the physical LAN.

# Decision

The platform will not use dynamic Docker network connections after container deployment.

Services will use:

Individual Docker Compose networks.
Host physical IP communication when required.

Example:

Grafana → Observability Node IP → Prometheus
Grafana → Observability Node IP → Loki

# Lessons Learned

For future Infrastructure as Code implementations:

Define external Docker networks inside docker-compose.yml before deployment.
Avoid modifying container networking after services are running.
Validate routing behavior before applying network changes.

---

# Future Considerations

All future application services should prioritize container deployment unless there is a specific operational reason to use native installation.
