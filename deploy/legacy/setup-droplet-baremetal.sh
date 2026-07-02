#!/usr/bin/env bash
# Legacy bare-metal Droplet setup (systemd + host nginx).
# Prefer Docker: REPO_URL=... bash deploy/docker/setup-droplet.sh
set -euo pipefail

APP_DIR="/var/www/weldingproject"
ENV_DIR="/etc/weldingproject"
REPO_URL="${REPO_URL:-}"

if [[ $EUID -ne 0 ]]; then
    echo "Run as root."
    exit 1
fi

apt-get update
apt-get install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git

if [[ -z "${REPO_URL}" ]]; then
    echo "Set REPO_URL before running, e.g.:"
    echo "  REPO_URL=git@github.com:user/weldingProject.git bash deploy/legacy/setup-droplet-baremetal.sh"
    exit 1
fi

mkdir -p "${APP_DIR}" "${ENV_DIR}"

if [[ ! -d "${APP_DIR}/.git" ]]; then
    git clone "${REPO_URL}" "${APP_DIR}"
fi

cd "${APP_DIR}"

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

if [[ ! -f "${ENV_DIR}/.env" ]]; then
    cp .env.example "${ENV_DIR}/.env"
    chmod 600 "${ENV_DIR}/.env"
    echo ""
    echo "Edit ${ENV_DIR}/.env with production values before continuing."
    echo "Required: SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, DATABASE_URL, SMTP."
    exit 0
fi

chown -R www-data:www-data "${APP_DIR}"
mkdir -p "${APP_DIR}/media"
chown -R www-data:www-data "${APP_DIR}/media"

set -a
# shellcheck disable=SC1091
source "${ENV_DIR}/.env"
set +a

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"

.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput

cp deploy/nginx/weldingproject.conf /etc/nginx/sites-available/weldingproject
ln -sf /etc/nginx/sites-available/weldingproject /etc/nginx/sites-enabled/weldingproject
rm -f /etc/nginx/sites-enabled/default
nginx -t

cp deploy/systemd/gunicorn.service /etc/systemd/system/gunicorn.service
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn
systemctl restart nginx

echo ""
echo "Next steps:"
echo "  1. certbot --nginx -d khodakmetal.co.uk -d www.khodakmetal.co.uk"
echo "  2. sudo -u www-data bash -c 'cd ${APP_DIR} && .venv/bin/python manage.py createsuperuser'"
echo "  3. Point DNS A-record to this server's IP"
