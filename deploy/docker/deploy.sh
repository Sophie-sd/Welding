#!/usr/bin/env bash
# Deploy / update Docker stack on DigitalOcean Droplet.
# Run from project root: bash deploy/docker/deploy.sh
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "${APP_DIR}"

USE_HTTPS="${USE_HTTPS:-false}"
if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
    USE_HTTPS="${USE_HTTPS:-false}"
fi

COMPOSE=(docker compose -f docker-compose.yml)
if [[ "${USE_HTTPS}" == "true" ]]; then
    COMPOSE+=(-f docker-compose.prod.yml)
fi

free_host_ports() {
    if [[ $EUID -eq 0 ]]; then
        systemctl stop nginx gunicorn gunicorn.service 2>/dev/null || true
        systemctl disable nginx gunicorn gunicorn.service 2>/dev/null || true
    else
        sudo systemctl stop nginx gunicorn gunicorn.service 2>/dev/null || true
        sudo systemctl disable nginx gunicorn gunicorn.service 2>/dev/null || true
    fi
}

echo "==> Free host ports 80/443 (stop bare-metal nginx/gunicorn)"
free_host_ports

echo "==> Build and start containers"
"${COMPOSE[@]}" build web nginx
"${COMPOSE[@]}" up -d

echo "==> Wait for healthcheck"
for _ in $(seq 1 30); do
    if curl -sf http://127.0.0.1/healthz/ >/dev/null 2>&1; then
        echo "HTTP healthcheck OK"
        break
    fi
    sleep 2
done

if ! curl -sf http://127.0.0.1/healthz/ >/dev/null 2>&1; then
    echo "ERROR: /healthz/ failed"
    "${COMPOSE[@]}" logs --tail=40 web nginx
    exit 1
fi

if [[ "${USE_HTTPS}" == "true" ]]; then
    if curl -sfk https://127.0.0.1/healthz/ >/dev/null 2>&1; then
        echo "HTTPS healthcheck OK"
    else
        echo "WARN: HTTPS healthcheck failed — check certbot paths in docker.prod.conf"
        "${COMPOSE[@]}" logs --tail=20 nginx
    fi
fi

"${COMPOSE[@]}" ps
echo "Deploy complete."
