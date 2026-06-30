#!/bin/sh
fail=0
V=/root/mesh/virtualservice.yaml
grep -q "kind: VirtualService" "$V" 2>/dev/null && grep -q "weight:" "$V" 2>/dev/null && echo "STEP:weighted traffic split:PASS" || { echo "STEP:weighted traffic split:FAIL:add a VirtualService with weights"; fail=1; }
grep -q "kind: PeerAuthentication" /root/mesh/peerauth.yaml 2>/dev/null && grep -qi "STRICT" /root/mesh/peerauth.yaml 2>/dev/null && echo "STEP:STRICT mTLS:PASS" || { echo "STEP:STRICT mTLS:FAIL:enforce STRICT mTLS"; fail=1; }
exit $fail
