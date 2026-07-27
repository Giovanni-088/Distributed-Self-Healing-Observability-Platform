# Troubleshooting Guide

## Network Connectivity Issue

## Problem

A server was unable to communicate correctly with the network.

Symptoms:

* No valid IP address assigned.
* DNS resolution failures.
* External connectivity unavailable.

---

# Diagnosis Process

## 1. Check Network Interfaces

Command:

```bash
ip addr
```

Observed issue:

The network interface did not have a valid IP configuration.

---

## 2. Verify Routing Table

Command:

```bash
ip route
```

Problem identified:

The default gateway configuration was incorrect.

Expected gateway:

```
192.168.1.x54
```

---

## 3. Verify DNS Resolution

Commands:

```bash
ping google.com
```

and

```bash
nslookup google.com
```

Result:

DNS requests failed because network routing was not correctly configured.

---

# Resolution

The network configuration was corrected by assigning:

```
Network:
192.168.1.0/24

Gateway:
192.168.1.x54

Static IP:
Configured according to node assignment
```

After applying the configuration:

* Interface received a valid IP.
* Gateway became reachable.
* DNS resolution recovered.

---

# Lessons Learned

## Validate Layer by Layer

Troubleshooting followed the OSI model:

1. Physical/interface state.
2. IP configuration.
3. Routing.
4. DNS resolution.
5. Application connectivity.

## Avoid Assuming Network Defaults

Incorrect gateway configurations can cause:

* Loss of external connectivity.
* DNS failures.
* Service deployment problems.

Network validation should be completed before deploying application services.

---

# Real Incident: Distributed Network Troubleshooting

## Problem

The observability deployment experienced multiple connectivity issues during initial configuration.

---

# Issue 1: Network Interface Without IP

## Symptoms

- Network interface was active but had no IPv4 address.
- Routing table was empty.
- DNS resolution failed.

## Diagnosis

Commands:

```bash
ip addr
ip route
```

The interface existed but no network configuration was applied.

# Root Cause

The network configuration was not applied correctly.

# Fix

Temporary network configuration was applied to restore connectivity.

Afterwards:

Installed network configuration tools.
Applied static network configuration.

# Lesson

Always validate:

Interface state.
IP assignment.
Routing table.
DNS resolution.

## Issue 2: Incorrect Gateway

# Symptoms

Network communication failed with:

No route to host

# Diagnosis

The assumed gateway did not match the actual network configuration.

Verification was performed using:

ip route get 8.8.8.8

and the physical network configuration.

# Root Cause

The default gateway was incorrectly assumed.

# Fix

Updated the network configuration with the correct gateway.

# Lesson

Never assume default gateway values.
Always verify the real network topology.

## Issue 3: Prometheus Container Unable To Reach Targets

# Symptoms

Host connectivity worked.
Prometheus container could not scrape external targets.

# Root Cause

The command:

nft flush ruleset

removed Docker-managed NAT rules.

Without Docker NAT masquerading:

Containers lost external connectivity.
Prometheus could not reach monitored nodes.

# Fix

Restart Docker:

systemctl restart docker

Docker regenerated required networking rules.

# Lesson

Never flush all nftables rules on Docker hosts.

## Issue 4: Service Accessible Locally But Not From LAN

# Symptoms

Services worked locally:

curl localhost:<port>

but failed from other devices.

# Diagnosis

ICMP worked, but TCP connections timed out.

# Root Cause

Firewall rules only allowed SSH traffic.

Monitoring service ports were blocked.

# Fix

Added required service ports:

Grafana.
Prometheus.
Loki.
Alertmanager.
Node Exporter.

# Lesson

A running service does not guarantee network accessibility.
Always validate:

Application status.
Local connectivity.
Firewall permissions.
External access.

---
