# Security Configuration

## Overview

Security controls are applied at the operating system and container layers to reduce attack surface and protect infrastructure services.

Implemented components:

* nftables firewall.
* Fail2ban.
* SSH key authentication.
* Trivy vulnerability scanning.

---

# nftables Firewall

## Purpose

nftables provides host-level traffic filtering.

The firewall follows a default-deny approach:

```text
Incoming traffic: DROP
```

Only required services are allowed.

---

# Allowed Traffic

| Port | Service       | Reason                 |
| ---- | ------------- | ---------------------- |
| 22   | SSH           | Server administration  |
| 80   | HTTP          | Nginx web traffic      |
| 443  | HTTPS         | Secure web traffic     |
| 8080 | cAdvisor      | Container metrics      |
| 9100 | Node Exporter | Infrastructure metrics |

Additional rule:

```text
ICMP echo-request
```

Used for network diagnostics.
---
# Observability Server Firewall Rules

The Observability Server uses nftables with a default deny policy.

Default behavior:

```text
Incoming traffic: DROP
```
Allowed services:

| Port | Service       |
| ---- | ------------- |
| 22   | SSH           |
| 3000 | Grafana       |
| 9090 | Prometheus    |
| 9093 | Alertmanager  |
| 3100 | Loki          |
| 9100 | Node Exporter |

# Docker Forward Chain Consideration

The Docker networking subsystem requires packet forwarding.

The forward chain must remain:

policy accept

Changing this policy to DROP can block traffic to Docker published ports even when services are running correctly.

Reason:

Docker NAT traffic passes through the forward chain before reaching containers.

# Firewall Management Warning

Avoid executing:

nft flush ruleset

on systems running Docker.

This command removes all nftables rules, including Docker-managed NAT rules.

Recommended approach:

nft -f /etc/nftables.conf

or flushing only the custom firewall table:

nft flush table inet filter

---

# Fail2ban

## Purpose

Fail2ban protects SSH access by detecting repeated failed authentication attempts.

Configuration:

```text
/etc/fail2ban/jail.local
```

Applied configuration:

```text
bantime = 1h
```

Enabled jail:

```text
[sshd]
enabled = true
```

Verification:

```bash
fail2ban-client status sshd
```

---

# Trivy

## Purpose

Trivy provides security scanning for container images.

It is used to:

* Detect known vulnerabilities.
* Identify CVEs before deployment.
* Improve container security practices.

Verification:

```bash
trivy --version
```

---

# Security Principles

The platform follows:

* Least privilege access.
* Minimal exposed services.
* Automated vulnerability scanning.
* Secure remote administration.
* Container security validation.
