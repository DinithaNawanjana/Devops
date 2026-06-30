#!/usr/bin/env bash
# Verify every Linux project's validate.sh passes against its reference
# solution. Runs each in an isolated temp dir with /root remapped.
set -u
BASE="$(cd "$(dirname "$0")/.." && pwd)/content/projects/linux"

declare -A SCRIPT=(
  [03-log-analyzer]=loganalyze.sh
  [04-user-manager]=usermgr.sh
  [05-disk-alert]=diskalert.sh
  [06-service-watcher]=watch.sh
  [07-file-organizer]=organize.sh
  [08-cron-report]=genreport.sh
  [09-admin-menu]=admin.sh
  [10-bootstrapper]=bootstrap.sh
)

overall=0
for dir in 03-log-analyzer 04-user-manager 05-disk-alert 06-service-watcher \
           07-file-organizer 08-cron-report 09-admin-menu 10-bootstrapper; do
  P="$BASE/$dir"
  T="$(mktemp -d)"
  name="${SCRIPT[$dir]}"
  sed "s#/root#$T#g" "$P/setup.sh"    > "$T/setup.sh"
  sed "s#/root#$T#g" "$P/validate.sh" > "$T/validate.sh"
  # setup runs first (mirrors the container: setup.sh fires before the learner
  # writes their script), then we drop in the reference solution.
  ( cd "$T" && sh setup.sh )
  sed "s#/root#$T#g" "$P/.solution.sh" > "$T/$name"; chmod +x "$T/$name"
  out="$( cd "$T" && sh validate.sh 2>&1 )"; code=$?
  if [ "$code" -eq 0 ]; then
    echo "✅ $dir"
  else
    echo "❌ $dir (exit $code)"; echo "$out" | sed 's/^/    /'
    overall=1
  fi
  rm -rf "$T"
done
exit $overall
