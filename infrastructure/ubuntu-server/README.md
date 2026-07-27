# Ubuntu Server Infrastructure

## Overview

This document describes the base configuration of the Ubuntu Server node used as the **Application + Automation Server** within the Distributed Self-Healing Observability Platform.

The server is responsible for:

* Running containerized applications.
* Hosting reverse proxy services.
* Providing container metrics.
* Exporting infrastructure metrics.
* Executing automation workloads.
* Hosting the future Self-Healing Engine.

---

# Server Information

| Parameter            | Value                           |
| -------------------- | ------------------------------- |
| Role                 | Application + Automation Server |
| Operating System     | Ubuntu Server 24.04 LTS         |
| IP Address           | 192.168.1.x5                    |
| Container Runtime    | Docker Engine                   |
| Container Management | Docker Compose                  |

---

# Installed Components

## Docker Engine

Docker is used as the main container runtime for all application and monitoring services.

### Installed Packages

* docker-ce
* docker-ce-cli
* containerd.io
* docker-buildx-plugin
* docker-compose-plugin

### Verification

```bash
docker --version
docker compose version
```

---

# Containerized Services

## Nginx Reverse Proxy

### Purpose

Nginx provides the entry point for HTTP/HTTPS traffic and will route requests to internal applications as the platform grows.

### Deployment Method

Nginx is deployed as a Docker container instead of a native package installation.

### Container Image

```text
nginx:stable-alpine
```

### Exposed Ports

| Port | Protocol | Purpose            |
| ---- | -------- | ------------------ |
| 80   | HTTP     | Web traffic        |
| 443  | HTTPS    | Secure web traffic |

### Configuration Location

```text
docker/nginx/
├── docker-compose.yml
└── nginx.conf
```

### Health Check

```bash
curl -I http://localhost
```

---

# cAdvisor

## Purpose

cAdvisor provides container-level resource monitoring.

Collected metrics include:

* CPU usage.
* Memory consumption.
* Filesystem usage.
* Container statistics.

### Container Image

```text
gcr.io/cadvisor/cadvisor:latest
```

### Exposed Port

| Port | Protocol | Purpose                     |
| ---- | -------- | --------------------------- |
| 8080 | HTTP     | Container metrics interface |

### Required Mounts

cAdvisor requires access to:

* Docker runtime information.
* Host filesystem.
* Kernel metrics.

Configuration:

```text
/var/run
/sys
/var/lib/docker
/dev/disk
```

### Health Check

```bash
curl -I http://localhost:8080
```

---

# Node Exporter

## Purpose

Node Exporter exposes Linux host metrics for Prometheus monitoring.

Collected metrics:

* CPU.
* RAM.
* Disk.
* Filesystem.
* Network.

### Container Image

```text
prom/node-exporter:latest
```

### Network Mode

```text
host
```

### Exposed Port

| Port | Protocol | Purpose            |
| ---- | -------- | ------------------ |
| 9100 | HTTP     | Prometheus metrics |

### Health Check

```bash
curl http://localhost:9100/metrics
```

---

# Security Components

## Fail2ban

### Purpose

Fail2ban protects SSH access by detecting and blocking repeated authentication failures.

### Configuration

Main configuration:

```text
/etc/fail2ban/jail.local
```

Applied settings:

```text
bantime = 1h
```

Enabled jail:

```text
sshd
```

### Verification

```bash
fail2ban-client status sshd
```

---

# nftables Firewall

## Purpose

nftables provides host-level firewall filtering.

Default policy:

```text
DROP
```

Only required services are allowed.

---

## Allowed Ports

| Port | Service       |
| ---- | ------------- |
| 22   | SSH           |
| 80   | HTTP          |
| 443  | HTTPS         |
| 8080 | cAdvisor      |
| 9100 | Node Exporter |

ICMP echo requests are also allowed for network diagnostics.

---

# Vulnerability Scanning

## Trivy

### Purpose

Trivy is used to scan container images and identify security vulnerabilities.

Capabilities:

* CVE detection.
* Container image analysis.
* Security validation before deployment.

Verification:

```bash
trivy --version
```

---

# Python Watchdog Environment

## Purpose

The Self-Healing Engine will use Python to monitor services and execute automated recovery actions.

Current status:

Base environment created.

Future capabilities:

* Docker health monitoring.
* Failure detection.
* Automatic recovery.
* Notification system.

---

## Python Environment

Location:

```text
watchdog/
```

Virtual environment:

```bash
python3 -m venv venv
```

Installed dependencies:

* docker
* python-telegram-bot
* requests

Requirements file:

```text
requirements.txt
```

---

# Exposed Services Summary

| Service       | Deployment | Port   |
| ------------- | ---------- | ------ |
| SSH           | Native     | 22     |
| Nginx         | Docker     | 80/443 |
| cAdvisor      | Docker     | 8080   |
| Node Exporter | Docker     | 9100   |

---

# Current Status

Completed:

* Docker Engine installation.
* Docker Compose configuration.
* Nginx container deployment.
* cAdvisor deployment.
* Node Exporter deployment.
* nftables firewall configuration.
* Fail2ban SSH protection.
* Trivy installation.
* Python Watchdog environment preparation.

Pending:

* Self-Healing Engine development.
* Application deployments.
* CI/CD integration.
* Ansible automation.

## Resilience Status

Verified:

- Docker enabled at boot.
- nftables enabled at boot.
- Fail2ban enabled at boot.
- Static network configuration persistent.
- health-check.service enabled.

Post-reboot behavior:

- Docker containers recover automatically.
- Health validation executes automatically.
- Results are stored in persistent logs.

---
