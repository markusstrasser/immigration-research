#!/usr/bin/env bash
# Repo-root entry point for immigration data reproducibility.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec bash "$REPO/infra/immigration-fiscal/reproduce.sh" "$@"
