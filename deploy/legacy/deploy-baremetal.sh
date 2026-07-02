#!/usr/bin/env bash
# Legacy bare-metal deploy (systemd + host nginx).
# Prefer Docker: bash deploy/docker/deploy.sh
set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/weldingproject}"
VENV_DIR="${APP_DIR}/.venv"
ENV_FILE="${ENV_FILE:-/etc/weldingproject/.env}"

cd "${APP_DIR}"

if [[ -f "${ENV_FILE}" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "${ENV_FILE}"
    set +a
fi

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"

git pull origin main

"${VENV_DIR}/bin/pip" install -r requirements.txt --quiet
"${VENV_DIR}/bin/python" manage.py migrate --noinput
"${VENV_DIR}/bin/python" manage.py collectstatic --noinput

sudo systemctl restart gunicorn
sudo systemctl reload nginx

echo "Deploy complete."
