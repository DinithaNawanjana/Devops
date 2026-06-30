#!/bin/sh
cd /root/ms 2>/dev/null || { echo "STEP:ms dir exists:FAIL:/root/ms missing"; exit 1; }
fail=0
froms=$(grep -ci "^FROM " Dockerfile 2>/dev/null)
[ "${froms:-0}" -ge 2 ] && echo "STEP:two or more build stages:PASS" || { echo "STEP:two or more build stages:FAIL:need >=2 FROM stages"; fail=1; }
grep -qiE "AS +builder" Dockerfile 2>/dev/null && echo "STEP:named builder stage:PASS" || { echo "STEP:named builder stage:FAIL:name the first stage 'AS builder'"; fail=1; }
grep -qi "COPY --from=" Dockerfile 2>/dev/null && echo "STEP:COPY --from between stages:PASS" || { echo "STEP:COPY --from between stages:FAIL:use COPY --from=builder"; fail=1; }
tail -n 20 Dockerfile | grep -qi "FROM alpine" && echo "STEP:final stage is alpine:PASS" || { echo "STEP:final stage is alpine:FAIL:final stage should be alpine"; fail=1; }
if docker info >/dev/null 2>&1; then
  if docker build -q -t lab_ms . >/dev/null 2>&1; then
    docker run --rm lab_ms 2>/dev/null | grep -qi "built artifact" && echo "STEP:[runtime] artifact copied & runs:PASS" || { echo "STEP:[runtime] artifact copied & runs:FAIL:output missing"; fail=1; }
  else echo "STEP:[runtime] image builds:FAIL:build failed"; fail=1; fi
  docker rmi -f lab_ms >/dev/null 2>&1
fi
exit $fail
