#!/usr/bin/env bash
# Runs ON the VDS. Only swaps the site files; Caddy config is managed by hand.
set -euo pipefail
WEBROOT="/var/www/centro-plus"
NEW="$WEBROOT.new"

[ -d "$NEW" ] || { echo "no new release uploaded"; exit 1; }
rm -rf "$WEBROOT.old"
[ -d "$WEBROOT" ] && mv "$WEBROOT" "$WEBROOT.old"
mv "$NEW" "$WEBROOT"
rm -rf "$WEBROOT.old"
chmod -R a+rX "$WEBROOT"
echo "[deploy] $(find "$WEBROOT" -type f | wc -l) files published to $WEBROOT"
