#!/usr/bin/env bash
# Issue or renew Let's Encrypt certs via webroot (works while Docker nginx holds :80).
# Run as root on the Droplet: bash deploy/docker/ssl-renew.sh [--force]
set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/weldingproject}"
WEBROOT="${WEBROOT:-/var/www/certbot}"
DOMAINS=(-d khodakmetal.com -d www.khodakmetal.com)
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

cd "${APP_DIR}"

if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

COMPOSE=(docker compose -f docker-compose.yml)
if [[ "${USE_HTTPS:-false}" == "true" ]]; then
    COMPOSE+=(-f docker-compose.prod.yml)
fi

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

ensure_webroot_lineage() {
    local conf="/etc/letsencrypt/renewal/khodakmetal.com.conf"
    if [[ ! -f "${conf}" ]]; then
        return 0
    fi
    # Prefer webroot over standalone so renewals work with Docker on :80.
    if grep -q 'authenticator = standalone' "${conf}"; then
        sed -i \
            -e 's/^authenticator = standalone$/authenticator = webroot/' \
            -e '/^\[\[webroot_map\]\]/,/^\[/{/^\[\[webroot_map\]\]/d;}' \
            "${conf}" || true
    fi
    if ! grep -q '^webroot_path' "${conf}"; then
        # Insert under [renewalparams]
        awk -v root="${WEBROOT}" '
            BEGIN { inserted=0 }
            /^\[renewalparams\]/ { print; print "authenticator = webroot"; print "webroot_path = " root; inserted=1; next }
            /^authenticator = / { if (inserted) next }
            /^webroot_path = / { next }
            { print }
        ' "${conf}" > "${conf}.tmp" && mv "${conf}.tmp" "${conf}"
    else
        sed -i "s|^webroot_path = .*|webroot_path = ${WEBROOT}|" "${conf}"
    fi
    if ! grep -q '^\[\[webroot_map\]\]' "${conf}"; then
        cat >> "${conf}" <<EOF

[[webroot_map]]
khodakmetal.com = ${WEBROOT}
www.khodakmetal.com = ${WEBROOT}
EOF
    fi
}

install_hooks
systemctl enable --now certbot.timer >/dev/null 2>&1 || true

if [[ ! -d /etc/letsencrypt/live/khodakmetal.com ]]; then
    echo "==> Issuing new certificate (webroot)"
    certbot certonly --webroot -w "${WEBROOT}" "${DOMAINS[@]}" \
        --agree-tos --non-interactive --keep-until-expiring \
        --email "${CERTBOT_EMAIL:-khodakmetalsolution@gmail.com}" \
        --deploy-hook /etc/letsencrypt/renewal-hooks/deploy/reload-welding-nginx.sh
else
    ensure_webroot_lineage
    if [[ "${FORCE}" == "true" ]]; then
        echo "==> Force renewing certificate (webroot)"
        certbot certonly --webroot -w "${WEBROOT}" "${DOMAINS[@]}" \
            --force-renewal --non-interactive \
            --deploy-hook /etc/letsencrypt/renewal-hooks/deploy/reload-welding-nginx.sh
    else
        echo "==> Renewing if due (webroot)"
        certbot renew --webroot -w "${WEBROOT}" --non-interactive
    fi
fi

ensure_webroot_lineage
certbot certificates
echo "SSL renew path OK (webroot + certbot.timer + nginx reload hook)."
