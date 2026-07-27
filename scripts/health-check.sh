#!/bin/bash
echo "=== $(hostname) — $(date) ==="
echo "--- Docker containers ---"
docker ps --format "table {{.Names}}\t{{.Status}}"
echo ""
echo "--- Health checks (auto-detectado) ---"

declare -A HEALTH_PATH=(
  [loki]="/ready"
  [prometheus]="/-/healthy"
  [alertmanager]="/-/healthy"
  [grafana]="/api/health"
  [node-exporter]="/metrics"
  [cadvisor]="/metrics"
  [nginx]="/"
)

declare -A HOST_NET_PORT=(
  [node-exporter]="9100"
)

for name in $(docker ps --format '{{.Names}}'); do
  path="${HEALTH_PATH[$name]:-/}"
  ports=$(docker port "$name" 2>/dev/null | grep '0.0.0.0' | sed -E 's/.*:([0-9]+)$/\1/' | sort -u)

  if [ -z "$ports" ] && [ -n "${HOST_NET_PORT[$name]}" ]; then
    ports="${HOST_NET_PORT[$name]}"
  fi

  if [ -z "$ports" ]; then
    echo "$name: sin puerto expuesto (interno / host network sin mapeo conocido)"
    continue
  fi

  for port in $ports; do
    if curl -sf --max-time 3 "http://localhost:${port}${path}" > /dev/null; then
      echo "$name (:$port$path): OK"
    else
      echo "$name (:$port$path): FALLO"
    fi
  done
done
