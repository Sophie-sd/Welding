#!/usr/bin/env bash
# Wrapper: deploy via Docker (recommended).
set -euo pipefail
exec bash "$(dirname "$0")/docker/deploy.sh" "$@"
