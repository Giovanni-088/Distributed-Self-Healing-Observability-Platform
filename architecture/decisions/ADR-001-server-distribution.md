# ADR-001: Server Distribution Strategy

## Status

Accepted

## Date

2026-07-27

---

# Context

The project requires a distributed architecture capable of simulating a real DevOps/SRE environment.

A single server could execute all components, but this approach would not represent real-world infrastructure patterns and would create a dependency between application workloads and monitoring systems.

To improve isolation and reliability, responsibilities were distributed across three independent nodes.

---

# Decision

The infrastructure was divided into:

## Ubuntu Server

Role:

Application + Automation Server

Responsibilities:

* Run Docker workloads.
* Execute automation.
* Host self-healing mechanisms.
* Manage application services.

IP:

```
192.168.1.75
```

---

## HP Debian

Role:

Observability Server

Responsibilities:

* Collect metrics.
* Store logs.
* Provide dashboards.
* Manage alerts.

Services:

* Prometheus.
* Grafana.
* Loki.
* Alertmanager.

IP:

```
192.168.1.78
```

---

## Toshiba NB200 Debian

Role:

Edge Monitoring Node

Responsibilities:

* Simulate remote infrastructure.
* Export hardware metrics.
* Provide distributed monitoring data.

IP:

```
192.168.1.77
```

---

# Reasons

## Isolation

Monitoring infrastructure remains independent from application workloads.

## Realistic Architecture

The design represents common production patterns where:

* Applications.
* Monitoring.
* Edge infrastructure.

operate independently.

## Scalability

New nodes can be integrated without redesigning the entire platform.

---

# Consequences

## Positive

* Better fault isolation.
* More realistic SRE environment.
* Easier troubleshooting.
* Independent maintenance.

## Negative

* Additional network configuration.
* More services to manage.
* Higher operational complexity.
