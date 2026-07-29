# Toshiba Edge Monitoring Node

## Overview

The Edge Monitoring Node is responsible for exposing infrastructure metrics from low-resource hardware.

Unlike the other nodes, this server runs native Prometheus exporters instead of Docker containers due to its operating system architecture.

## Installed Components

- Debian 12 (Bookworm)
- Node Exporter
- Blackbox Exporter
- nftables
- Fail2ban
- OpenSSH

## Network

- Static IP configured using **ifupdown**
- Persistent network configuration
- Dedicated monitoring ports exposed through nftables

## Security

- SSH key authentication only
- Root login disabled
- Password authentication disabled
- Dedicated service accounts for exporters
- nftables default-deny policy
- Fail2ban protection enabled

## Monitoring Services

### Node Exporter

- Native binary
- Managed by systemd
- Starts automatically at boot

### Blackbox Exporter

- Native binary
- Managed by systemd
- ICMP probing enabled using Linux capabilities instead of root privileges

## Service Resilience

The Edge Monitoring Node does not run the Python Watchdog because it does not host Docker workloads.

Instead, resilience is implemented directly through systemd.

Both monitoring services are configured with automatic restart policies:

- `Restart=always`
- `RestartSec=5`

This allows the operating system to recover failed services automatically without requiring an additional monitoring application.

The solution provides a lightweight self-healing mechanism appropriate for a resource-constrained system.

## Status

Current platform validation:

- Node Exporter reachable
- Blackbox Exporter reachable
- Edge node successfully scraped by Prometheus
- Integrated into the centralized observability platform
