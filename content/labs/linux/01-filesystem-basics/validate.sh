#!/bin/sh
# Validation contract: print one STEP line per check, exit 0 only if all pass.
#   STEP:<name>:PASS
#   STEP:<name>:FAIL[:message]
cd /root 2>/dev/null || cd / 2>/dev/null

fail=0

# Step 1 — directory tree
if [ -d project/src ] && [ -d project/docs ]; then
  echo "STEP:Project tree (project/src, project/docs):PASS"
else
  echo "STEP:Project tree (project/src, project/docs):FAIL:run mkdir -p project/src project/docs"
  fail=1
fi

# Step 2 — README contains hello
if [ -f project/README.md ] && grep -qi "hello" project/README.md; then
  echo "STEP:README.md contains 'hello':PASS"
else
  echo "STEP:README.md contains 'hello':FAIL:create project/README.md with the word hello"
  fail=1
fi

# Step 3 — run.sh is mode 755
if [ -f project/src/run.sh ]; then
  mode=$(stat -c "%a" project/src/run.sh 2>/dev/null)
  if [ "$mode" = "755" ]; then
    echo "STEP:run.sh is executable (755):PASS"
  else
    echo "STEP:run.sh is executable (755):FAIL:got mode $mode, expected 755"
    fail=1
  fi
else
  echo "STEP:run.sh is executable (755):FAIL:project/src/run.sh missing"
  fail=1
fi

# Step 4 — secret.txt is mode 600
if [ -f project/secret.txt ]; then
  mode=$(stat -c "%a" project/secret.txt 2>/dev/null)
  if [ "$mode" = "600" ]; then
    echo "STEP:secret.txt is owner-only (600):PASS"
  else
    echo "STEP:secret.txt is owner-only (600):FAIL:got mode $mode, expected 600"
    fail=1
  fi
else
  echo "STEP:secret.txt is owner-only (600):FAIL:create project/secret.txt and chmod 600"
  fail=1
fi

exit $fail
