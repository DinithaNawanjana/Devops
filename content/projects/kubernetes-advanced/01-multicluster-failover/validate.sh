#!/bin/sh
fail=0
n=$(grep -l "kind: Cluster" /root/mc/cluster-*.yaml 2>/dev/null | wc -l)
[ "${n:-0}" -ge 2 ] && echo "STEP:two kind clusters defined:PASS" || { echo "STEP:two kind clusters defined:FAIL:add primary + standby cluster configs"; fail=1; }
[ -x /root/mc/failover.sh ] && grep -q "use-context" /root/mc/failover.sh 2>/dev/null && echo "STEP:failover switches context:PASS" || { echo "STEP:failover switches context:FAIL:failover.sh should switch kubectl context"; fail=1; }
exit $fail
