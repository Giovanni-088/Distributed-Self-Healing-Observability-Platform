# Installed Stack

The HP Debian node works as the centralized Observability Server.

The complete monitoring stack is deployed using Docker Engine and Docker Compose Plugin.

All services use independent Docker Compose files and are configured with:

restart: unless-stopped


# Deployed Services

| Service       | Purpose                            | Port | Deployment |
| ------------- | ---------------------------------- | ---- | ---------- |
| Prometheus    | Metrics collection and alert rules | 9090 | Docker     |
| Grafana       | Dashboards and visualization       | 3000 | Docker     |
| Alertmanager  | Alert routing and notifications    | 9093 | Docker     |
| Loki          | Log aggregation                    | 3100 | Docker     |
| Node Exporter | Host metrics exporter              | 9100 | Docker     |
| Promtail      | Log collector                      | 9080 | Docker     |


# Directory Structure
~/observability/

├── prometheus/
│   └── docker-compose.yml
│
├── node-exporter/
│   └── docker-compose.yml
│
├── grafana/
│   └── docker-compose.yml
│
├── alertmanager/
│   └── docker-compose.yml
│
├── loki/
│   └── docker-compose.yml
│
└── promtail/
    └── docker-compose.yml

---

# Status

Current deployment status:

| Component | Status |
|---|---|
| Prometheus | Running |
| Grafana | Running |
| Alertmanager | Running |
| Loki | Running |
| Node Exporter | Running |
| Promtail | Running |

---

# Prometheus Targets Validation

Current targets:

| Target | Status |
|---|---|
| Observability Node | UP |
| Prometheus | UP |
| Application Node | UP |
| Edge Node | DOWN (Expected - pending deployment) |

The edge node is expected to remain unavailable until its monitoring services are deployed.
