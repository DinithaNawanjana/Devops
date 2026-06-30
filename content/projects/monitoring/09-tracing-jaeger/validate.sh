#!/bin/sh
fail=0
grep -qiE "jaeger|otel" /root/mon/docker-compose.yml 2>/dev/null && echo "STEP:tracing backend running:PASS" || { echo "STEP:tracing backend running:FAIL:run jaeger or an otel collector"; fail=1; }
grep -qiE "otlp|otel|jaeger" /root/mon/otel-config.yml 2>/dev/null && echo "STEP:traces exported:PASS" || { echo "STEP:traces exported:FAIL:export traces to the backend"; fail=1; }
exit $fail
