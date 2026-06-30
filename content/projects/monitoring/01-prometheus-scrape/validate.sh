#!/bin/sh
F=/root/mon/prometheus.yml
fail=0
[ -f "$F" ] && echo "STEP:prometheus.yml exists:PASS" || { echo "STEP:prometheus.yml exists:FAIL:create mon/prometheus.yml"; exit 1; }
grep -q "scrape_configs:" "$F" && echo "STEP:has scrape_configs:PASS" || { echo "STEP:has scrape_configs:FAIL:add scrape_configs"; fail=1; }
grep -q "job_name" "$F" && grep -q "targets" "$F" && echo "STEP:defines a job with targets:PASS" || { echo "STEP:defines a job with targets:FAIL:add a job_name and targets"; fail=1; }
exit $fail
