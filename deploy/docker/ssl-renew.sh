#!/usr/bin/env bash
# Issue or renew Let's Encrypt certs via webroot (works while Docker nginx holds :80).
# Run as root on the Droplet: bash deploy/docker/ssl-renew.sh [--force]
set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/weldingproject}"
WEBROOT="${WEBROOT:-/var/www/certbot}"
EMAIL="${CERTBOT_EMAIL:-khodakmetalsolution@gmail.com}"
FORCE=false

for arg in "$@"; do
    case "${arg}" in
        --force) FORCE=true ;;
        *)
            echo "Unknown argument: ${arg}"
            exit 1
            ;;
    esac
done

if [[ $EUID -ne 0 ]]; then
    echo "Run as root."
    exit 1
fi

mkdir -p "${WEBROOT}/.well-known/acme-challenge"
chmod -R 755 "${WEBROOT}"

install_hooks() {
    mkdir -p /etc/letsencrypt/renewal-hooks/deploy
    cat > /etc/letsencrypt/renewal-hooks/deploy/reload-welding-nginx.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="/var/www/weldingproject"
cd "${APP_DIR}"
COMPOSE=(docker compose -f docker-compose.yml)
if grep -q '^USE_HTTPS=true' .env 2>/dev/null; then
    COMPOSE+=(-f docker-compose.prod.yml)
fi
"${COMPOSE[@]}" exec -T nginx nginx -s reload \
    || "${COMPOSE[@]}" restart nginx
EOF
    chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-welding-nginx.sh
}

install_hooks
systemctl enable --now certbot.timer >/dev/null 2>&1 || true

CERTBOT_ARGS=(
    certonly
    --webroot
    -w "${WEBROOT}"
    -d khodakmetal.com
    -d www.khodakmetal.com
    --agree-tos
    --non-interactive
    --email "${EMAIL}"
    --deploy-hook /etc/letsencrypt/renewal-hooks/deploy/reload-welding-nginx.sh
)

if [[ ! -d /etc/letsencrypt/live/khodakmetal.com ]]; then
    echo "==> Issuing new certificate (webroot)"
    certbot "${CERTBOT_ARGS[@]}"
elif [[ "${FORCE}" == "true" ]]; then
    echo "==> Force renewing certificate (webroot)"
    certbot "${CERTBOT_ARGS[@]}" --force-renewal
else
    echo "==> Renewing if due (webroot)"
    # Re-run certonly without force so lineage switches to webroot authenticator.
    certbot "${CERTBOT_ARGS[@]}" --keep-until-expiring
fi

# Ensure timer renewals use webroot (rewrite if still standalone).
RENEW_CONF="/etc/letsencrypt/renewal/khodakmetal.com.conf"
if [[ -f "${RENEW_CONF}" ]]; then
    sed -i 's/^authenticator = standalone$/authenticator = webroot/' "${RENEW_CONF}"
    if grep -q '^webroot_path' "${RENEW_CONF}"; then
        sed -i "s|^webroot_path = .*|webroot_path = ${WEBROOT}|" "${RENEW_CONF}"
    else
        awk -v root="${WEBROOT}" '
            /^\[renewalparams\]/ { print; print "webroot_path = " root; next }
            { print }
        ' "${RENEW_CONF}" > "${RENEW_CONF}.tmp" && mv "${RENEW_CONF}.tmp" "${RENEW_CONF}"
    fi
    if ! grep -q '^\[\[webroot_map\]\]' "${RENEW_CONF}"; then
        printf '\n[[webroot_map]]\nkhodakmetal.com = %s\nwww.khodakmetal.com = %s\n' \
            "${WEBROOT}" "${WEBROOT}" >> "${RENEW_CONF}"
    fi
fi

echo "==> Dry-run renewal"
certbot renew --dry-run

certbot certificates
echo "SSL OK: webroot + certbot.timer + nginx reload hook."
