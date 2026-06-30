#!/bin/sh
fail=0
J=/root/ansible/templates/site.conf.j2
[ -f "$J" ] && grep -q "{{" "$J" && echo "STEP:Jinja2 template with a variable:PASS" || { echo "STEP:Jinja2 template with a variable:FAIL:create templates/site.conf.j2 with {{ var }}"; fail=1; }
P=/root/ansible/template.yml
[ -f "$P" ] && grep -q "template:" "$P" && echo "STEP:uses the template module:PASS" || { echo "STEP:uses the template module:FAIL:use ansible template module"; fail=1; }
grep -q "vars:" "$P" 2>/dev/null && echo "STEP:defines variables:PASS" || { echo "STEP:defines variables:FAIL:define vars: in the play"; fail=1; }
exit $fail
