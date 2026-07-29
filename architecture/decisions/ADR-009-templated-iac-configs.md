# ADR-009: Versioned Configuration Templates

## Status

Accepted

## Context

Infrastructure services require multiple configuration files such as Docker Compose definitions, Prometheus configuration, and reverse proxy settings.

Keeping these files only on deployed servers would make infrastructure recovery dependent on the server state.

## Decision

All service configurations are maintained as version-controlled Jinja2 templates inside the repository.

Deployment playbooks generate the final configuration directly from these templates.

## Rationale

- Git becomes the single source of truth.
- Entire environments can be recreated from scratch.
- Configuration drift is minimized.
- Infrastructure remains reproducible.

## Consequences

Changes are performed by modifying templates rather than editing production servers manually.

Future deployments automatically inherit configuration improvements through version control.
