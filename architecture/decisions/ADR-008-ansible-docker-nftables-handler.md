# ADR-008: Automatic Docker Restart After Firewall Reload

## Status

Accepted

## Context

Reloading nftables removes Docker-managed networking rules, causing container connectivity failures.

Initially, the issue was resolved manually by restarting Docker after every firewall update.

## Decision

The Ansible hardening playbook automatically chains a Docker restart whenever firewall rules are reloaded and Docker is present.

## Rationale

Embedding the solution into the automation eliminates recurring operational failures and preserves Infrastructure as Code principles.

## Consequences

Firewall updates remain fully automated while Docker networking is restored automatically whenever required.

The solution is idempotent and safely ignored on hosts where Docker is not installed.
