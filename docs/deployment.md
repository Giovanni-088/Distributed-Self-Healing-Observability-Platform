# Deployment Documentation

## Network Configuration

The platform operates inside a local network using a dedicated subnet.

## Network Parameters

| Parameter     | Value          |
| ------------- | -------------- |
| Network       | 192.168.1.0/24 |
| Gateway       | 192.168.1.x54  |
| IP Assignment | Static         |

---

# Node Configuration

## Ubuntu Server

Role:

Application + Automation Server

| Parameter  | Value                   |
| ---------- | ----------------------- |
| Hostname   | ubuntu-server           |
| IP Address | 192.168.1.x5            |
| OS         | Ubuntu Server 24.04 LTS |

Services:

| Service | Port |
| ------- | ---- |
| SSH     | 22   |
| HTTP    | 80   |
| HTTPS   | 443  |

---

## Toshiba NB200

Role:

Edge Monitoring Node

| Parameter  | Value        |
| ---------- | ------------ |
| Hostname   | toshiba-edge |
| IP Address | 192.168.1.x7 |
| OS         | Debian       |

Services:

| Service           | Port |
| ----------------- | ---- |
| SSH               | 22   |
| Node Exporter     | 9100 |
| Blackbox Exporter | 9115 |

## Edge Node Network Configuration

The Edge Monitoring Node uses the traditional **ifupdown** networking stack instead of Netplan.

Static addressing is configured through `/etc/network/interfaces`, providing persistent network configuration across reboots.

Unlike the Ubuntu Server, no Netplan configuration is required on this node.

---

## HP Debian

Role:

Observability Server

| Parameter  | Value            |
| ---------- | ---------------- |
| Hostname   | hp-observability |
| IP Address | 192.168.1.x8     |
| OS         | Debian           |

Services:

| Service      | Port |
| ------------ | ---- |
| SSH          | 22   |
| Grafana      | 3000 |
| Prometheus   | 9090 |
| Alertmanager | 9093 |
| Loki         | 3100 |

---

# Deployment Order

The platform should be deployed in the following order:

## 1. Infrastructure Layer

Configure:

* Linux systems.
* Static IP addresses.
* SSH access.
* Network connectivity.

---

## 2. Ubuntu Server

Install:

* Docker Engine.
* Docker Compose.
* Automation tools.
* Security configuration.

---

## 3. Observability Server

Deploy:

* Prometheus.
* Grafana.
* Alertmanager.
* Loki.
* Promtail.

---

## 4. Edge Node

Deploy:

* Node Exporter.
* Blackbox Exporter.

Register metrics in Prometheus.

---

## 5. Self-Healing Engine

Deploy:

* Python Watchdog.
* Docker API integration.
* Notification services.

---

# Required Connectivity

The following communication paths must be available:

```text
Ubuntu
 |
 | Metrics
 v

HP Debian

```

```text
Toshiba
 |
 | Metrics
 v

HP Debian
```

```text
HP Debian
 |
 | Alerts
 v

Ubuntu Watchdog
```
---

# Network Configuration

The platform operates inside a local network using a static IP configuration.

Parameter	Value
Network	192.168.1.0/24
Gateway	192.168.1.x54
Addressing	Static IP

# Gateway Configuration

The infrastructure uses a static network configuration.

The default gateway is verified against the physical network configuration instead of assuming common defaults.

Configured gateway:

```text
<LOCAL_GATEWAY>
```

---

## Service Ports

# Ubuntu Server

Node: Application + Automation Server

IP Address:

192.168.1.x8
Service	Port	Protocol	Deployment
SSH	22	TCP	Native
Nginx	80	TCP	Docker
Nginx HTTPS	443	TCP	Docker
cAdvisor	8080	TCP	Docker
Node Exporter	9100	TCP	Docker

# HP Debian

Node: Observability Server

IP Address:

192.168.1.x8

Role:

Centralized Monitoring Infrastructure

| Service | Port | Protocol | Deployment |
|---|---|---|---|
| SSH | 22 | TCP | Native |
| Grafana | 3000 | TCP | Docker |
| Prometheus | 9090 | TCP | Docker |
| Alertmanager | 9093 | TCP | Docker |
| Loki | 3100 | TCP | Docker |
| Node Exporter | 9100 | TCP | Docker |

# Toshiba NB200

Node: Edge Monitoring Node

IP Address:

192.168.1.x7
Service	Port	Protocol
SSH	22	TCP
Node Exporter	9100	TCP
Blackbox Exporter	9115	TCP
Network Communication
Monitoring Flow
Ubuntu Server
      |
      | Metrics
      v
HP Observability Server
Toshiba Edge Node
      |
      | Metrics
      v


## HP Observability Server

# Deployment Validation

Required checks:

Verify SSH connectivity between nodes.
Validate static IP configuration.
Confirm firewall rules.
Verify exposed ports.
Confirm monitoring endpoints are reachable.

Example:

curl http://192.168.1.x5:9100/metrics

---

# Resilience and Automatic Startup

## Overview

The platform is designed to recover automatically after system reboot or unexpected shutdown.

The objective is to restore all infrastructure components without manual intervention.

The recovery chain is based on:

- Docker restart policies.
- Systemd service activation.
- Persistent network configuration.
- Automatic health validation.

---

# Container Recovery

All Docker Compose services use:

```yaml
restart: unless-stopped
```

This ensures containers automatically start when the Docker daemon becomes available after boot.

Affected services:

Nginx.
Prometheus.
Grafana.
Loki.
Alertmanager.
Node Exporter.
Promtail.
cAdvisor.

# System Services

The following services are enabled during system startup:

| Service  | Purpose              |
| -------- | -------------------- |
| Docker   | Container runtime    |
| nftables | Firewall persistence |
| Fail2ban | SSH protection       |

Verification:

systemctl is-enabled <service>

Expected output:

enabled

# Network Persistence

Static network configuration is maintained using Netplan.

The configuration persists after reboot and automatically restores:

Static IP addressing.
Default gateway.
DNS configuration.

Configuration location:

/etc/netplan/*.yaml

After modifications:

sudo netplan apply

# Post-Boot Health Validation

health-check.service

A systemd service executes the health validation script automatically after network and Docker initialization.

Location:

/etc/systemd/system/health-check.service

The service is node-specific and is configured locally on each server.

#Systemd Unit

[Unit]
Description=Health check post-boot
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/home/<user>/Distributed-Self-Healing-Observability-Platform/scripts/health-check.sh
StandardOutput=append:/var/log/health-check.log
StandardError=append:/var/log/health-check.log

[Install]
WantedBy=multi-user.target

# Enable Service

Commands:

sudo systemctl daemon-reload
sudo systemctl enable health-check.service
sudo systemctl start health-check.service

Logs:

cat /var/log/health-check.log

# Git SSH Configuration

Each infrastructure node uses an independent SSH key for GitHub authentication.

Current model:

| Node                 | SSH Key              |
| -------------------- | -------------------- |
| Application Server   | Dedicated device key |
| Observability Server | Dedicated device key |

Private keys are never shared between servers.

Daily workflow:

git pull

git add .

git commit -m "message"

git push

---

## Automation with Ansible

Infrastructure provisioning and configuration management are automated using Ansible.

The Application Server acts as the control node, managing all infrastructure from a single location.

### Inventory Design

The inventory is organized by infrastructure role:

- Application Server
- Observability Server
- Edge Monitoring Node
- Docker Hosts (group)

The Application Server is managed locally, while remote nodes are accessed through SSH.

Group variables are used to customize firewall rules, service deployment, and host-specific configuration without duplicating playbooks.

### Passwordless Privilege Escalation

Automation requires passwordless privilege escalation.

Each managed node grants passwordless sudo through a dedicated sudoers configuration, allowing Ansible to execute privileged tasks non-interactively while maintaining a controlled security model.

___

### Docker Deployment

Docker installation is fully automated through `docker.yml`.

The playbook:

- Installs Docker Engine.
- Installs the Compose Plugin.
- Configures the official Docker repository.
- Adds the appropriate local user to the Docker group.
- Supports both Ubuntu and Debian using Ansible facts.

The playbook is idempotent, allowing repeated executions without changing an already compliant system.

---

### Monitoring Deployment

Monitoring services are deployed through a single playbook containing multiple plays.

```text
Inventory
      │
      ▼
Groups
      │
      ▼
monitoring.yml
      │
      ├── Application Server
      │       ├── Nginx
      │       ├── cAdvisor
      │       └── Node Exporter
      │
      └── Observability Server
              ├── Prometheus
              ├── Grafana
              ├── Alertmanager
              ├── Loki
              ├── Promtail
              └── Node Exporter
```

Each infrastructure role receives only the services appropriate for that node while sharing a common deployment workflow.

---

## Phase 6 Summary

Infrastructure automation has been successfully implemented.

The complete Ubuntu Server and Observability Server environments can now be rebuilt from scratch using three playbooks:

- `hardening.yml`
- `docker.yml`
- `monitoring.yml`

This establishes Git as the single source of truth for infrastructure configuration and fulfills the Infrastructure as Code objective of the project.

---

# Validation Checklist

Before continuing:

* [x] All nodes reachable by SSH.
* [x] Static IP configuration verified.
* [x] Gateway reachable.
* [x] DNS resolution working.
* [x] Required ports accessible.
* [x] Monitoring services reachable.
