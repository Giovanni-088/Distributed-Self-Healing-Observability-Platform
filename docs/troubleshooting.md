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

# Loki Startup Delay and Health Endpoint Validation

## Problem

During health-check development, Loki initially returned:

```text
503 Ingester not ready
```

# Diagnosis

The issue was not caused by:

Incorrect configuration.
Failed deployment.
Health-check script errors.

Loki requires an internal initialization period before becoming fully ready.

# Root Cause

Loki performs a warm-up process during startup.

Immediately after container creation, the service may reject health requests until internal components finish initialization.

# Fix

The solution was waiting for the normal startup period instead of modifying the configuration or health-check logic.

# Lesson

Health checks must consider application startup behavior.

A temporary unhealthy state after boot does not always indicate a failure.

# Service Health Endpoint Validation

## Problem

The root endpoint (/) was not a reliable health check for several services.

# Diagnosis

Different services expose dedicated health endpoints.

# Final Health Mapping

| Service       | Endpoint      |
| ------------- | ------------- |
| Loki          | `/ready`      |
| Prometheus    | `/-/healthy`  |
| Alertmanager  | `/-/healthy`  |
| Grafana       | `/api/health` |
| Node Exporter | `/metrics`    |
| cAdvisor      | `/metrics`    |

# Lesson

Health validation should use application-specific endpoints instead of generic HTTP checks.

---

## Docker Repository Reports Unsupported Architecture

### Problem

Docker packages could not be installed because no installation candidate was available.

### Diagnosis

The Docker repository was correctly configured for the detected system architecture.

### Root Cause

The operating system was installed as **i386**, while Docker CE only distributes packages for supported architectures such as amd64.

The processor itself supports 64-bit execution, but the installed operating system does not.

### Resolution

The platform architecture was adapted to use native Prometheus exporters instead of Docker containers on the Edge Monitoring Node.

### Lesson Learned

Unexpected package manager output may reveal underlying platform characteristics rather than configuration errors. Always verify the detected architecture before assuming a repository misconfiguration.

---

## systemd Environment Variables Not Loaded

### Problem

The watchdog service started successfully, but Telegram notifications were never delivered.

### Diagnosis

Systemd ignored the environment variables defined in the external configuration file.

### Root Cause

The environment file used shell syntax (`export KEY=value`), while systemd expects plain `KEY=value` assignments.

The service continued running because the notification module was intentionally designed to fail safely when credentials are unavailable.

### Resolution

Rewrite the environment file using the syntax expected by systemd and verify the loaded variables from the running process environment.

### Lesson Learned

Files with the `.env` extension are not interpreted identically by every application. Always verify the expected syntax for the runtime environment instead of assuming shell-compatible behavior.

---

## Python Virtual Environment Could Not Be Created

### Problem

Creating a Python virtual environment failed because `ensurepip` was unavailable.

### Diagnosis

The operating system did not include the Python virtual environment package by default.

### Root Cause

Some Debian installations require the corresponding `python3-venv` package to be installed separately.

### Resolution

Install the appropriate virtual environment package for the installed Python version and recreate the virtual environment.

### Lesson Learned

Do not assume Python development packages are installed by default across different Linux distributions. Verify package availability during deployment.

---

## SSH Key Distribution Failed After SSH Hardening

### Problem

Automated SSH key deployment using `ssh-copy-id` failed.

### Diagnosis

Authentication attempts were rejected even though the destination hosts were reachable.

### Root Cause

Password authentication had already been disabled as part of the SSH hardening process.

Since `ssh-copy-id` relies on password authentication during the initial bootstrap, it could no longer install the new automation key.

### Resolution

The public key was installed manually using an already authenticated management session.

### Lesson Learned

Automation keys should be deployed before disabling password authentication, or an alternative authenticated management channel should already be available.

## nftables Reload Broke Docker Networking

### Problem

Container networking stopped working immediately after applying firewall changes through Ansible.

### Diagnosis

Docker containers lost external connectivity and published ports became unreachable.

### Root Cause

Reloading the firewall configuration removed Docker-managed NAT rules.

Although the custom firewall configuration remained valid, Docker's networking rules had to be recreated.

### Resolution

The Ansible handler chain was updated so that every firewall reload automatically restarts Docker when Docker is installed.

### Lesson Learned

Infrastructure automation should permanently solve recurring operational issues.

A manual fix is not considered complete until it is incorporated into the automation workflow itself.

---

## community.general.capabilities Always Reports Changes

### Problem

The `community.general.capabilities` module reported a change during every execution, even when the required capability had already been applied.

### Root Cause

This module does not always detect existing Linux file capabilities with complete idempotency.

### Impact

The capability remains correctly configured, but Ansible may still report the task as changed.

### Resolution

No corrective action is required.

This behavior is a known limitation of the module rather than a problem with the playbook implementation.

---

## Environment Variables Available in Bash but Missing in Python

### Problem

The AI analyzer reported that required environment variables were missing even though they were visible in the interactive shell.

### Root Cause

Variables loaded with `source` were not exported to child processes because the environment file followed systemd's `EnvironmentFile` syntax.

### Resolution

For manual execution:

```bash
set -a
source ~/.watchdog_env
set +a
python3 incident_analyzer.py
```

This exports all loaded variables to child processes while keeping production configuration compatible with systemd.

---
