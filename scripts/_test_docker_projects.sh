#!/usr/bin/env bash
# Verify every Docker project's STRUCTURAL checks pass against its reference
# artifacts. Runtime steps are docker-guarded, so with no daemon present they
# are skipped and only structural grading runs (which is what we assert here).
# In the dind lab sandbox the same validators additionally run the build/run
# checks. Flow per project: setup -> solution_cmds -> validate, /root remapped.
set -u
BASE="$(cd "$(dirname "$0")/.." && pwd)/content/projects/docker"

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
  if [ "$code" -eq 0 ]; then
    echo "✅ $dir ($(echo "$out" | grep -c PASS) structural checks)"
  else
    echo "❌ $dir (exit $code)"; echo "$out" | sed 's/^/    /'; overall=1
  fi
  rm -rf "$T"
done
exit $overall
