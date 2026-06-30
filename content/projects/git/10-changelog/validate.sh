#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -x changelog.sh ] && [ -f CHANGELOG.md ]; then echo "STEP:changelog.sh produced CHANGELOG.md:PASS"; else echo "STEP:changelog.sh produced CHANGELOG.md:FAIL:create and run changelog.sh"; fail=1; fi
miss=""
for s in "feat: add login" "fix: correct typo" "feat: add logout"; do
  grep -qF "$s" CHANGELOG.md 2>/dev/null || miss="$miss; $s"
done
if [ -z "$miss" ]; then echo "STEP:all commit subjects listed:PASS"; else echo "STEP:all commit subjects listed:FAIL:missing$miss"; fail=1; fi
exit $fail
