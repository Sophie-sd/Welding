#!/usr/bin/env bash
# Initial DigitalOcean Droplet setup (Ubuntu 24.04, Docker).
# Run as root: REPO_URL=git@github.com:user/weldingProject.git bash deploy/docker/setup-droplet.sh
set -euo pipefail

APP_DIR="/var/www/weldingproject"
REPO_URL="${REPO_URL:-}"

if [[ $EUID -ne 0 ]]; then
    echo "Run as root."
    exit 1
fi

if [[ -z "${REPO_URL}" ]]; then
    echo "Set REPO_URL before running, e.g.:"
    echo "  REPO_URL=git@github.com:user/weldingProject.git bash deploy/docker/setup-droplet.sh"
    exit 1
fi

apt-get update
apt-get install -y git ufw certbot curl

ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "==> Stop legacy bare-metal stack (if present)"
systemctl stop gunicorn nginx 2>/dev/null || true
systemctl disable gunicorn nginx 2>/dev/null || true

bash "$(dirname "$0")/install-docker.sh"

mkdir -p /var/www
if [[ ! -d "${APP_DIR}/.git" ]]; then
    git clone "${REPO_URL}" "${APP_DIR}"
fi

cd "${APP_DIR}"

if [[ ! -f .env ]]; then
    cp .env.docker.example .env
    chmod 600 .env
    echo ""
    echo "Edit ${APP_DIR}/.env before continuing:"
    echo "  SECRET_KEY, POSTGRES_PASSWORD, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, SMTP"
    echo ""
    echo "Then run: bash deploy/docker/deploy.sh"
    exit 0
fi

bash deploy/docker/deploy.sh

echo ""
echo "Next steps:"
echo "  1. Point DNS A-records (@ and www) to this Droplet IP"
echo "  2. Verify HTTP: curl -sf http://127.0.0.1/healthz/"
echo "  3. SSL:"
echo "       docker compose -f docker-compose.yml -f docker-compose.prod.yml stop nginx"
echo "       certbot certonly --standalone -d khodakmetal.com -d www.khodakmetal.com"
echo "       # set USE_HTTPS=true in .env"
echo "       bash deploy/docker/deploy.sh"
echo "  4. Superuser:"
echo "       docker compose exec web python manage.py createsuperuser"
