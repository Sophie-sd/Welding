#!/usr/bin/env bash
# Wrapper: DigitalOcean Droplet setup via Docker (recommended).
set -euo pipefail
exec bash "$(dirname "$0")/docker/setup-droplet.sh" "$@"
