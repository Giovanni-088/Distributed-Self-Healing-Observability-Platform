# Observability Stack Configuration

## Prometheus

Prometheus is deployed as the central metrics collection system.

Configuration file:

prometheus.yml

Global configuration:

global:
  scrape_interval: 15s

# Scrape Targets

Prometheus monitors the following nodes:

| Target             | Metrics                  |
| ------------------ | ------------------------ |
| Application Node   | Node Exporter + cAdvisor |
| Observability Node | Node Exporter            |
| Edge Node          | Node Exporter            |
| Prometheus         | Internal metrics         |

# Important Configuration Note

Prometheus runs inside a Docker container.

Because of container networking isolation:

localhost

inside the Prometheus container refers only to the Prometheus container itself.

For this reason, the observability node is referenced using its physical network address instead of localhost.

Example:

<OBSERVABILITY_NODE_IP>:9090

# Promtail

Promtail is responsible for collecting Docker container logs.

Configuration:

server:
  http_listen_port: 9080

Logs are collected from:

/var/lib/docker/containers/

and forwarded to Loki.

# Loki Integration

Loki receives logs collected by Promtail.

Communication flow:

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

---
