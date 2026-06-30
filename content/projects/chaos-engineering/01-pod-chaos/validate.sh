#!/bin/sh
F=/root/chaos/podchaos.yaml
fail=0
grep -q "kind: PodChaos" "$F" 2>/dev/null && echo "STEP:PodChaos experiment:PASS" || { echo "STEP:PodChaos experiment:FAIL:create a PodChaos"; exit 1; }
grep -q "pod-kill" "$F" && echo "STEP:pod-kill action:PASS" || { echo "STEP:pod-kill action:FAIL:use action pod-kill"; fail=1; }
grep -q "selector:" "$F" && echo "STEP:targets a selector:PASS" || { echo "STEP:targets a selector:FAIL:add a selector"; fail=1; }
exit $fail
