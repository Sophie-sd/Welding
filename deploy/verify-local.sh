#!/usr/bin/env bash
# Local pre-deploy verification. Run from project root.
set -euo pipefail

cd "$(dirname "$0")/.."

source .venv/bin/activate 2>/dev/null || {
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt -q
}

export DJANGO_SETTINGS_MODULE=config.settings.production
export SECRET_KEY="local-verify-key-with-enough-length-and-randomness-12345"
export ALLOWED_HOSTS="localhost,127.0.0.1"
export SECURE_SSL_REDIRECT="False"
python manage.py check --deploy

echo "==> Migrations"
python manage.py migrate --noinput

echo "==> Collectstatic"
python manage.py collectstatic --noinput

echo "==> Tests"
python manage.py test pages

REQUIRED_IMAGES=(
    logo-khodak.png
    hero-home.png
    hero-about.png
    hero-contact.png
    project-frame.png
    heavy-industrial-frame-source.png
    project-tig.png
    portfolio-omega.png
    portfolio-nexus.png
    portfolio-bridge.png
    portfolio-residential.png
    workshop.png
    tig-weld.png
    hero-faq.png
    hero-portfolio.png
    hero-blog.png
    welder.png
    blueprints.png
    placeholder.png
)

echo "==> Static images"
missing=0
for img in "${REQUIRED_IMAGES[@]}"; do
    if [[ ! -f "static/images/${img}" ]]; then
        echo "MISSING: static/images/${img}"
        missing=1
    fi
done
if [[ "${missing}" -eq 1 ]]; then
    exit 1
fi
echo "All ${#REQUIRED_IMAGES[@]} images present."

echo ""
echo "Local verification passed."
echo "Docker deploy: cp .env.docker.example .env && bash deploy/docker/deploy.sh"
echo "Droplet setup: REPO_URL=<your-repo> bash deploy/docker/setup-droplet.sh"
