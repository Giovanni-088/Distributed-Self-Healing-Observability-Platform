# Distributed Self-Healing Observability Platform

Distributed observability and self-healing platform designed to monitor containerized services, automatically detect failures, and execute recovery processes within an architecture inspired by DevOps/SRE practices.

The project implements a distributed infrastructure using multiple Linux nodes with separated responsibilities:

* **Application & Automation Server**
* **Observability Server**
* **Edge Monitoring Node**

The goal is to build an environment where infrastructure can be monitored, analyzed, and automatically recovered through automation, observability, and security practices.

---

# Architecture

```text
                         LAN
                          |
                 Gateway 192.168.1.x54
                          |
        ---------------------------------------
        |                  |                  |
        |                  |                  |
 Ubuntu Server        HP Debian          Toshiba NB200
 192.168.1.x5         192.168.1.x8       192.168.1.x7

 Application          Observability      Edge Monitoring
 Automation           Server             Node

 Docker               Prometheus         Node Exporter
 Nginx                Grafana            Blackbox Exporter
 Watchdog             Loki
 Trivy                Alertmanager
```

---

# System Nodes

## Ubuntu Server

**Role:** Application + Automation Server

Responsibilities:

* Execution of containerized services.
* Docker application management.
* Task automation.
* Self-healing engine execution.
* Incident management.
* Reverse proxy using Nginx.
* Integration with DevOps tools.

IP Address:

```text
192.168.1.x5
```

---

## HP Debian

**Role:** Observability Server

Responsibilities:

* Centralized metrics collection.
* Infrastructure visualization.
* Alert management.
* Log storage.

Main services:

* Prometheus
* Grafana
* Alertmanager
* Loki
* Promtail

IP Address:

```text
192.168.1.x8
```

---

## Toshiba NB200 Debian

**Role:** Edge Monitoring Node

Responsibilities:

* Simulation of a remote physical node.
* Hardware metrics collection.
* Connectivity monitoring.
* Distributed architecture testing.

Services:

* Node Exporter
* Blackbox Exporter

IP Address:

```text
192.168.1.x7
```

---

# Main Features

## Observability

The platform provides:

* CPU, RAM, disk, and network monitoring.
* Docker container metrics.
* Centralized dashboards.
* Log collection and querying.
* Alert management.

Technology stack:

* Prometheus
* Grafana
* Loki
* Alertmanager
* Node Exporter
* cAdvisor

---

# Scripts and Utilities

## Universal Health Check

The project includes a universal health validation script:

```text
scripts/health-check.sh
```

The script is shared across all infrastructure nodes.

Instead of using different versions per server, it dynamically detects:

- Running Docker containers.
- Published ports.
- Available health endpoints.

# Supported Health Endpoints

| Service       | Endpoint      |
| ------------- | ------------- |
| Loki          | `/ready`      |
| Prometheus    | `/-/healthy`  |
| Alertmanager  | `/-/healthy`  |
| Grafana       | `/api/health` |
| Node Exporter | `/metrics`    |
| cAdvisor      | `/metrics`    |
| Nginx         | `/`           |

# Design Goal

Maintaining a single universal health-check script prevents configuration drift between nodes and avoids server-specific versions being overwritten during Git synchronization.

---

## Self-Healing

The system implements automated recovery mechanisms.

Workflow:

```text
Service Failure

      |
      v

Alert Detection

      |
      v

Alertmanager

      |
      v

Python Watchdog

      |
      v

Recovery Action

      |
      v

Incident Log
```

Capabilities:

* Detect stopped containers.
* Execute corrective actions.
* Restart services.
* Generate incident records.
* Send notifications.

---

# Security

The platform includes:

* SSH administration using key-based authentication.
* nftables-based firewall.
* Brute-force attack protection using Fail2ban.
* Vulnerability scanning with Trivy.
* Container security best practices.

---

# Automation and Infrastructure as Code

Tools used:

* Ansible
* Bash scripting
* Docker Compose
* GitHub Actions

Objectives:

* Reproducible configuration.
* Automated deployments.
* Automated validation.
* Simplified maintenance.

---

The infrastructure is fully reproducible through Ansible.

Four dedicated playbooks manage the complete platform lifecycle:

- **hardening.yml** — system hardening, firewall configuration, SSH hardening and security baseline.
- **docker.yml** — Docker Engine installation and configuration for containerized nodes.
- **monitoring.yml** — deployment of all monitoring and observability services.
- **edge.yml** — native deployment of exporters on the Edge Monitoring Node without Docker.

This approach allows the complete platform to be rebuilt from scratch without requiring undocumented manual configuration.

---
# Roadmap

---

# Roadmap

## Phase 0 — Infrastructure

- [x] Linux server provisioning
- [x] Static network configuration
- [x] SSH authentication
- [x] Repository initialization

---

## Phase 1 — Base Server

- [x] Operating system hardening
- [x] Docker Engine installation
- [x] Reverse proxy deployment
- [x] Development environment preparation

---

## Phase 2 — Observability

- [x] Prometheus
- [x] Grafana
- [x] Alertmanager
- [x] Metrics collection

---

## Phase 3 — Logging

- [x] Loki
- [x] Promtail
- [x] Centralized log collection

---

## Phase 4 — Distributed Self-Healing

- [x] Python Watchdog
- [x] Automatic container recovery
- [x] Telegram notifications
- [x] Incident logging
- [x] Distributed watchdog architecture

---

## Phase 5 — Security

- [x] SSH hardening
- [x] nftables
- [x] Fail2ban
- [x] Trivy

---

## Phase 6 — Infrastructure as Code

- [x] Ansible Control Node
- [x] System hardening automation
- [x] Docker deployment
- [x] Monitoring deployment
- [x] Native Edge deployment
- [x] Infrastructure templating

---

## Phase 7 — AI Layer

- [x] AI Incident Analyzer
- [x] Groq integration
- [x] Flapping detection
- [x] Automated incident summaries

---

## CI/CD

- [x] Python linting
- [x] Ansible validation
- [x] Trivy security scanning
- [x] Documented deployment workflow

---

# Technology Stack

## Infrastructure

* Linux
* Ubuntu Server
* Debian
* VMware Workstation
* SSH

## Containers

* Docker
* Docker Compose
* Nginx

## Observability

* Prometheus
* Grafana
* Loki
* Alertmanager
* Node Exporter
* cAdvisor

## Automation

* Python
* Ansible
* Bash
* GitHub Actions

## Security

* nftables
* Fail2ban
* Trivy

---

# Final Objective

Build a distributed platform capable of:

* Monitoring complete infrastructure.
* Automatically detecting failures.
* Generating alerts.
* Executing corrective actions.
* Maintaining service availability.
* Simulating a real SRE operational architecture.

# Project Status

The platform has reached its planned architecture and roadmap goals.

Current capabilities include:

- Distributed three-node architecture
- Infrastructure as Code with Ansible
- Centralized observability
- Automated self-healing
- Security hardening
- AI-powered incident analysis
- CI/CD validation pipelines

Every subsystem has been validated through real deployment, operational testing, and documented troubleshooting gathered during development rather than simulated examples.
