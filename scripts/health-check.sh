#!/bin/bash
echo "=== $(hostname) — $(date) ==="
echo "--- Docker ---"
docker ps --format "table {{.Names}}\t{{.Status}}"
echo "--- Puertos ---"
for port in 80 8080 9100; do
  curl -sf --max-time 3 http://localhost:$port > /dev/null && echo "puerto $port: OK" || echo "puerto $port: FALLO"
done
