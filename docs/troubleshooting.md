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
192.168.1.254
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
192.168.1.254

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
