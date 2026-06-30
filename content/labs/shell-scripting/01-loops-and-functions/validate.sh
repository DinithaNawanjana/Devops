#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
SCRIPT=./fizzbuzz.sh

# Step 1 — executable with shebang
if [ -f "$SCRIPT" ]; then
  mode=$(stat -c "%a" "$SCRIPT" 2>/dev/null)
  if [ "$mode" = "755" ] && head -1 "$SCRIPT" | grep -q "bin/bash"; then
    echo "STEP:Executable script with shebang:PASS"
  else
    echo "STEP:Executable script with shebang:FAIL:need mode 755 + #!/bin/bash (got $mode)"
    fail=1
  fi
else
  echo "STEP:Executable script with shebang:FAIL:/root/fizzbuzz.sh missing"
  echo "STEP:FizzBuzz output for 15:FAIL:no script"
  echo "STEP:Uses a classify function:FAIL:no script"
  echo "STEP:No-arg prints usage and fails:FAIL:no script"
  exit 1
fi

# Step 2 — correct output for N=15
OUT=$("$SCRIPT" 15 2>/dev/null)
expected="1
2
fizz
4
buzz
fizz
7
8
fizz
buzz
11
fizz
13
14
fizzbuzz"
if [ "$OUT" = "$expected" ]; then
  echo "STEP:FizzBuzz output for 15:PASS"
else
  echo "STEP:FizzBuzz output for 15:FAIL:output for './fizzbuzz.sh 15' did not match expected sequence"
  fail=1
fi

# Step 3 — defines a classify function
if grep -Eq 'classify *\(\)|function +classify' "$SCRIPT"; then
  echo "STEP:Uses a classify function:PASS"
else
  echo "STEP:Uses a classify function:FAIL:define a function named classify"
  fail=1
fi

# Step 4 — no-arg guard prints usage and exits non-zero
HELP=$("$SCRIPT" 2>&1)
code=$?
if echo "$HELP" | grep -qi "usage" && [ "$code" -ne 0 ]; then
  echo "STEP:No-arg prints usage and fails:PASS"
else
  echo "STEP:No-arg prints usage and fails:FAIL:with no arg, print 'usage' and exit non-zero (got code $code)"
  fail=1
fi

exit $fail
