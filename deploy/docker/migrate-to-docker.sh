#!/usr/bin/env bash
# Switch Droplet from bare-metal to Docker + PostgreSQL (PrometeyLabs pattern).
# Run as root on server: bash deploy/docker/migrate-to-docker.sh
set -euo pipefail

APP_DIR="/var/www/weldingproject"
LEGACY_ENV="/etc/weldingproject/.env"

if [[ $EUID -ne 0 ]]; then
    echo "Run as root."
    exit 1
fi

echo "==> Stop legacy bare-metal stack"
systemctl stop gunicorn nginx 2>/dev/null || true
systemctl disable gunicorn nginx 2>/dev/null || true

cd "${APP_DIR}"
git pull origin main

bash deploy/docker/install-docker.sh

if [[ ! -f .env ]]; then
    cp .env.docker.example .env
    chmod 600 .env

    if [[ -f "${LEGACY_ENV}" ]]; then
        echo ""
        echo "Legacy env found: ${LEGACY_ENV}"
        echo "Copy SECRET_KEY and SMTP values into ${APP_DIR}/.env manually."
        echo "Set POSTGRES_PASSWORD to a new strong password."
        echo ""
        grep -E '^(SECRET_KEY|EMAIL_|DEFAULT_FROM|QUOTE_)' "${LEGACY_ENV}" || true
    fi

    echo "Edit ${APP_DIR}/.env then run: bash deploy/docker/deploy.sh"
    exit 0
fi

bash deploy/docker/deploy.sh
