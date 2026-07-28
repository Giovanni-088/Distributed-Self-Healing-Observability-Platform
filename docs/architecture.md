# System Architecture

## Overview

Distributed Self-Healing Observability Platform is designed using a distributed architecture where each physical or virtual node has a specific responsibility.

The system separates application execution, observability and edge monitoring into independent components to simulate a real DevOps/SRE environment.

The architecture is composed of three Linux nodes:

* Ubuntu Server: Application and Automation Server.
* HP Debian: Central Observability Server.
* Toshiba NB200 Debian: Edge Monitoring Node.

This separation allows independent scaling, troubleshooting and maintenance of each component.

---

# Architecture Diagram

```text
                         LAN Network

                    Gateway
                 192.168.1.x54

                          |
        -----------------------------------------
        |                  |                    |
        |                  |                    |

 Ubuntu Server          HP Debian          Toshiba NB200
 192.168.1.x5           192.168.1.x8       192.168.1.x7

 Application            Observability      Edge Monitoring
 Automation             Server             Node

 Docker                 Prometheus         Node Exporter
 Nginx                  Grafana            Blackbox Exporter
 Watchdog               Loki
 Trivy                  Alertmanager
```

---

# Node Responsibilities

## Ubuntu Server

### Role

Application + Automation Server

### Main Responsibilities

* Host containerized applications.
* Execute Docker workloads.
* Run automation processes.
* Execute self-healing mechanisms.
* Manage recovery actions.
* Provide reverse proxy services.

### Main Components

* Docker Engine.
* Docker Compose.
* Nginx.
* Python Watchdog.
* cAdvisor.
* Node Exporter.
* Trivy.

### IP Address

```
192.168.1.x5
```

---

# HP Debian

## Role

Observability Server

The HP Debian machine works as the central monitoring platform.

### Main Responsibilities

* Collect infrastructure metrics.
* Store time-series data.
* Visualize system health.
* Manage alerts.
* Centralize logs.

### Main Components

## Prometheus

Responsible for:

* Metrics collection.
* Time-series database.
* Alert rules.

Port:

```
9090
```

---

## Grafana

Responsible for:

* Dashboards.
* Visualization.
* Monitoring panels.

Port:

```
3000
```

---

## Alertmanager

Responsible for:

* Alert processing.
* Notification routing.
* External integrations.

Port:

```
9093
```

---

## Loki

Responsible for:

* Centralized log storage.

Port:

```
3100
```

---

## Promtail

Responsible for:

* Collecting logs.
* Forwarding logs to Loki.

---

### IP Address

```
192.168.1.x8
```

---

# Toshiba NB200 Debian

## Role

Edge Monitoring Node

The Toshiba acts as a simulated remote physical server.

### Main Responsibilities

* Provide additional infrastructure metrics.
* Simulate distributed monitoring.
* Monitor hardware resources.

### Main Components

* Node Exporter.
* Blackbox Exporter.

Collected data:

* CPU.
* RAM.
* Disk.
* Network.
* Temperature.
* Connectivity.

### IP Address

```
192.168.1.x7
```

---

# Data Flow

## Metrics Flow

```text
Ubuntu / Toshiba

      |
      v

Node Exporter

      |
      v

Prometheus

      |
      v

Grafana
```

---

## Log Flow

```text
Docker Containers

        |
        v

Promtail

        |
        v

Loki

        |
        v

Grafana
```

---

## Self-Healing Flow

```text
Service Failure

        |
        v

Prometheus Detection

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
---

## Platform Deployment Summary

| Node | Runtime | Primary Services |
|------|---------|------------------|
| Ubuntu Server | Docker | Nginx, cAdvisor, Node Exporter |
| Observability Server | Docker | Prometheus, Grafana, Alertmanager, Loki, Promtail, Node Exporter |
| Edge Monitoring Node | Native binaries | Node Exporter, Blackbox Exporter |

The platform intentionally combines containerized workloads and native system services.

---

# Design Principles

## Separation of Responsibilities

Each node performs a dedicated function:

* Applications are isolated from monitoring workloads.
* Observability remains independent from application failures.
* Edge devices can be monitored remotely.

## Scalability

Additional nodes can be integrated by deploying monitoring agents and registering them in the observability stack.

## Reproducibility

The infrastructure is designed to be deployed using:

* Docker Compose.
* Ansible.
* GitHub Actions.
