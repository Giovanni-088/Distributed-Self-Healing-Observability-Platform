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

# Roadmap

## Phase 0 - Infrastructure

* [x] Linux server preparation.
* [x] Network configuration.
* [x] Static IP addressing.
* [x] SSH configuration.

---

## Phase 1 - Base Server

* [x] Ubuntu Server hardening.
* [x] System optimization/debloat.
* [x] Docker Engine installation.
* [x] DevOps environment preparation.

---

## Phase 2 - Observability

* [x] Prometheus installation.
* [x] Grafana installation.
* [x] Alertmanager configuration.
* [x] Metrics integration.

---

## Phase 3 - Logging

* [x] Loki implementation.
* [x] Promtail configuration.
* [x] Centralized log management.

---

## Phase 4 - Self-Healing Engine

* [ ] Python Watchdog development.
* [ ] Docker API integration.
* [ ] Automated recovery workflows.

---

## Phase 5 - Security

* [ ] SSH hardening.
* [ ] Firewall configuration.
* [ ] Fail2ban deployment.
* [ ] Trivy security scanning.

---

## Phase 6 - Automation

* [ ] Ansible playbooks.
* [ ] Maintenance scripts.
* [ ] CI/CD pipeline.

---

## Phase 7 - AI Layer

* [ ] Automated incident analysis.
* [ ] Intelligent alert explanation.
* [ ] Recovery recommendations.

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
