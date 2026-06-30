#!/bin/sh
cd /root/site 2>/dev/null || { echo "STEP:site dir exists:FAIL:/root/site missing"; exit 1; }
fail=0
if grep -qi "^FROM nginx" Dockerfile 2>/dev/null; then echo "STEP:Dockerfile FROM nginx:PASS"; else echo "STEP:Dockerfile FROM nginx:FAIL:base image should be nginx"; fail=1; fi
if grep -q "usr/share/nginx/html" Dockerfile 2>/dev/null; then echo "STEP:COPY into nginx web root:PASS"; else echo "STEP:COPY into nginx web root:FAIL:COPY html into /usr/share/nginx/html/"; fail=1; fi
if grep -qi "Hello Docker" html/index.html 2>/dev/null; then echo "STEP:index.html content:PASS"; else echo "STEP:index.html content:FAIL:html/index.html should say Hello Docker"; fail=1; fi
if docker info >/dev/null 2>&1; then
  docker rm -f lab_static >/dev/null 2>&1
  if docker build -q -t lab_static . >/dev/null 2>&1      && docker run -d --name lab_static -p 8081:80 lab_static >/dev/null 2>&1; then
    sleep 2
    if curl -s http://localhost:8081 | grep -qi "Hello Docker"; then echo "STEP:[runtime] site serves Hello Docker:PASS"; else echo "STEP:[runtime] site serves Hello Docker:FAIL:container did not serve the page"; fail=1; fi
  else
    echo "STEP:[runtime] image builds & runs:FAIL:docker build/run failed"; fail=1
  fi
  docker rm -f lab_static >/dev/null 2>&1
fi
exit $fail
