#!/bin/sh
F=/root/repo/Jenkinsfile
fail=0
[ -f "$F" ] && echo "STEP:Jenkinsfile exists:PASS" || { echo "STEP:Jenkinsfile exists:FAIL:create Jenkinsfile"; exit 1; }
grep -q "pipeline" "$F" && grep -q "stages" "$F" && echo "STEP:declarative pipeline with stages:PASS" || { echo "STEP:declarative pipeline with stages:FAIL:use pipeline { stages { } }"; fail=1; }
if grep -q "stage('Build')" "$F" && grep -q "stage('Test')" "$F" && grep -q "stage('Deploy')" "$F"; then echo "STEP:Build/Test/Deploy stages:PASS"; else echo "STEP:Build/Test/Deploy stages:FAIL:add Build, Test, Deploy stages"; fail=1; fi
exit $fail
