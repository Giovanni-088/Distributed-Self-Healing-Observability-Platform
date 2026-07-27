# Deployment Documentation

## Network Configuration

The platform operates inside a local network using a dedicated subnet.

## Network Parameters

| Parameter     | Value          |
| ------------- | -------------- |
| Network       | 192.168.1.0/24 |
| Gateway       | 192.168.1.254  |
| IP Assignment | Static         |

---

# Node Configuration

## Ubuntu Server

Role:

Application + Automation Server

| Parameter  | Value                   |
| ---------- | ----------------------- |
| Hostname   | ubuntu-server           |
| IP Address | 192.168.1.75            |
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
| IP Address | 192.168.1.77 |
| OS         | Debian       |

Services:

| Service           | Port |
| ----------------- | ---- |
| SSH               | 22   |
| Node Exporter     | 9100 |
| Blackbox Exporter | 9115 |

---

## HP Debian

Role:

Observability Server

| Parameter  | Value            |
| ---------- | ---------------- |
| Hostname   | hp-observability |
| IP Address | 192.168.1.78     |
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

# Validation Checklist

Before continuing:

* [ ] All nodes reachable by SSH.
* [ ] Static IP configuration verified.
* [ ] Gateway reachable.
* [ ] DNS resolution working.
* [ ] Required ports accessible.
* [ ] Monitoring services reachable.
