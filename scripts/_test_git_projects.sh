#!/usr/bin/env bash
# Verify every Git project's validate.sh passes against its reference solution.
# Flow per project: setup -> solution_cmds -> validate, in an isolated temp dir
# with /root remapped.
set -u
BASE="$(cd "$(dirname "$0")/.." && pwd)/content/projects/git"

overall=0
for P in "$BASE"/*/; do
  dir="$(basename "$P")"
  T="$(mktemp -d)"
  sed "s#/root#$T#g" "$P/setup.sh"     > "$T/setup.sh"
  sed "s#/root#$T#g" "$P/.solution.sh" > "$T/solution.sh"
  sed "s#/root#$T#g" "$P/validate.sh"  > "$T/validate.sh"
  ( cd "$T" && sh setup.sh >/dev/null 2>&1 )
  ( cd "$T" && bash solution.sh >/dev/null 2>&1 )
  out="$( cd "$T" && sh validate.sh 2>&1 )"; code=$?
  if [ "$code" -eq 0 ]; then
    echo "✅ $dir"
  else
    echo "❌ $dir (exit $code)"; echo "$out" | sed 's/^/    /'; overall=1
  fi
  rm -rf "$T"
done
exit $overall
