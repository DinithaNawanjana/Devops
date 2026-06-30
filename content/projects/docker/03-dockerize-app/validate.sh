#!/bin/sh
cd /root/app 2>/dev/null || { echo "STEP:app dir exists:FAIL:/root/app missing"; exit 1; }
fail=0
[ -f app.py ] && echo "STEP:app.py present:PASS" || { echo "STEP:app.py present:FAIL:create app.py"; fail=1; }
grep -qi "^FROM python" Dockerfile 2>/dev/null && echo "STEP:FROM python base:PASS" || { echo "STEP:FROM python base:FAIL:base on python image"; fail=1; }
grep -qi "EXPOSE 5000" Dockerfile 2>/dev/null && echo "STEP:EXPOSE 5000:PASS" || { echo "STEP:EXPOSE 5000:FAIL:EXPOSE 5000"; fail=1; }
grep -q "app.py" Dockerfile 2>/dev/null && grep -qiE "CMD|ENTRYPOINT" Dockerfile 2>/dev/null && echo "STEP:CMD runs app.py:PASS" || { echo "STEP:CMD runs app.py:FAIL:CMD should run app.py"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker rm -f lab_app >/dev/null 2>&1
  if docker build -q -t lab_app . >/dev/null 2>&1 && docker run -d --name lab_app -p 5000:5000 lab_app >/dev/null 2>&1; then
    sleep 2
    curl -s http://localhost:5000 | grep -qi "OK from app" && echo "STEP:[runtime] app responds:PASS" || { echo "STEP:[runtime] app responds:FAIL:no OK from app"; fail=1; }
  else echo "STEP:[runtime] image builds & runs:FAIL:build/run failed"; fail=1; fi
  docker rm -f lab_app >/dev/null 2>&1
fi
exit $fail
