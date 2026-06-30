#!/bin/sh
F=/root/tf/network.tf
fail=0
[ -f "$F" ] && echo "STEP:network.tf exists:PASS" || { echo "STEP:network.tf exists:FAIL:create tf/network.tf"; exit 1; }
grep -q 'resource "aws_vpc"' "$F" && echo "STEP:declares a VPC:PASS" || { echo "STEP:declares a VPC:FAIL:add an aws_vpc resource"; fail=1; }
grep -q 'resource "aws_subnet"' "$F" && echo "STEP:declares subnets:PASS" || { echo "STEP:declares subnets:FAIL:add aws_subnet resources"; fail=1; }
exit $fail
