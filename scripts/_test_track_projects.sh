#!/usr/bin/env bash
# Generic project test harness: setup -> reference solution -> validate, in an
# isolated temp dir with /root remapped. Usage:
#   scripts/_test_track_projects.sh <track>     # e.g. ansible, terraform
set -u
track="${1:?usage: _test_track_projects.sh <track>}"
BASE="$(cd "$(dirname "$0")/.." && pwd)/content/projects/$track"
[ -d "$BASE" ] || { echo "no such track: $BASE"; exit 2; }

overall=0
for P in "$BASE"/*/; do
  dir="$(basename "$P")"
  [ -f "$P/.solution.sh" ] || { echo "⚠️  $dir (no reference solution)"; continue; }
  T="$(mktemp -d)"
  sed "s#/root#$T#g" "$P/setup.sh"     > "$T/setup.sh"
  sed "s#/root#$T#g" "$P/.solution.sh" > "$T/solution.sh"
  sed "s#/root#$T#g" "$P/validate.sh"  > "$T/validate.sh"
  ( cd "$T" && sh setup.sh >/dev/null 2>&1 )
  ( cd "$T" && bash solution.sh >/dev/null 2>&1 )
  out="$( cd "$T" && sh validate.sh 2>&1 )"; code=$?
  if [ "$code" -eq 0 ]; then echo "✅ $dir"; else echo "❌ $dir (exit $code)"; echo "$out" | sed 's/^/    /'; overall=1; fi
  rm -rf "$T"
done
exit $overall
