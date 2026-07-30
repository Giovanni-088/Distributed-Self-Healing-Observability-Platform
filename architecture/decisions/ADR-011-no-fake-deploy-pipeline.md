# ADR-011 — No Fake Deployment Pipeline

## Status

Accepted

## Decision

Do not implement an automatic deployment workflow that cannot operate against the real infrastructure.

## Rationale

The project runs entirely inside a private on-premises network.

GitHub-hosted runners cannot reach the deployment targets.

Creating a fake deployment pipeline would misrepresent the actual architecture.

## Consequences

Deployment remains manual through documented Ansible commands while CI continues validating code quality and security.
