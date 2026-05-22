#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ "${1:-}" = "" ]; then
  echo "Usage: run-restore.command <backup-path>"
  exit 1
fi
exec python3 -m src.main --restore "$1"
