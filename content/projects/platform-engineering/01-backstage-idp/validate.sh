#!/bin/sh
fail=0
grep -q "kind: Component" /root/idp/catalog-info.yaml 2>/dev/null && grep -q "backstage.io" /root/idp/catalog-info.yaml 2>/dev/null && echo "STEP:Backstage Component:PASS" || { echo "STEP:Backstage Component:FAIL:add a backstage.io Component"; fail=1; }
grep -q "kind: Template" /root/idp/template.yaml 2>/dev/null && echo "STEP:scaffolder Template:PASS" || { echo "STEP:scaffolder Template:FAIL:add a Backstage Template"; fail=1; }
exit $fail
