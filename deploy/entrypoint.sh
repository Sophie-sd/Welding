#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for PostgreSQL..."
python <<'PY'
import os
import sys
import time

import psycopg

url = os.environ.get("DATABASE_URL", "")
if not url or url.startswith("sqlite"):
    sys.exit(0)

for attempt in range(30):
    try:
        psycopg.connect(url)
        print("==> DB ready")
        break
    except Exception:
        time.sleep(2)
else:
    print("FATAL: DB not ready")
    sys.exit(1)
PY

echo "==> Django check + migrate + collectstatic"
python manage.py check --deploy
python manage.py migrate --noinput
python manage.py collectstatic --noinput

_static_count="$(find "${STATIC_ROOT:-/app/staticfiles}" -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "==> static files: ${_static_count}"
if [[ "${_static_count:-0}" -lt 10 ]]; then
    echo "WARN: staticfiles count low — check STATIC_ROOT and collectstatic"
fi

exec "$@"
