#!/usr/bin/env bash
# Runs ON the VDS as user deploy: switches the "current" symlink to the uploaded release.
# Caddy serves /srv/centro-plus/current (config: deploy/Caddyfile.snippet, set up by root once).
set -euo pipefail
BASE=/srv/centro-plus
REL="$1"

[ -d "$BASE/releases/$REL" ] || { echo "no release $REL uploaded"; exit 1; }
chmod -R a+rX "$BASE/releases/$REL"
ln -sfn "releases/$REL" "$BASE/current.tmp" && mv -Tf "$BASE/current.tmp" "$BASE/current"
ls -1dt "$BASE"/releases/* | tail -n +4 | xargs -r rm -rf   # keep 3 releases
echo "[deploy] $(find "$BASE/current/" -type f | wc -l) files published from release $REL"
