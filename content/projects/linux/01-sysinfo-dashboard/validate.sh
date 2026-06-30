#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
SCRIPT=./sysinfo.sh

# Step 1 — script exists and is executable (755)
if [ -f "$SCRIPT" ]; then
  mode=$(stat -c "%a" "$SCRIPT" 2>/dev/null)
  if [ "$mode" = "755" ] && head -1 "$SCRIPT" | grep -q "bin/bash"; then
    echo "STEP:Executable script with shebang:PASS"
  else
    echo "STEP:Executable script with shebang:FAIL:need mode 755 and a #!/bin/bash shebang (got mode $mode)"
    fail=1
  fi
else
  echo "STEP:Executable script with shebang:FAIL:/root/sysinfo.sh missing"
  fail=1
fi

# Capture output once for the content checks. Run via its own shebang
# (the script is bash; invoking with sh would break bashisms).
OUT=$("$SCRIPT" 2>/dev/null)

# Step 2 — all four section headers present
missing=""
for s in HOSTNAME CPU MEMORY DISK; do
  echo "$OUT" | grep -qi "$s" || missing="$missing $s"
done
if [ -z "$missing" ]; then
  echo "STEP:All sections present (HOSTNAME, CPU, MEMORY, DISK):PASS"
else
  echo "STEP:All sections present (HOSTNAME, CPU, MEMORY, DISK):FAIL:missing$missing"
  fail=1
fi

# Step 3 — memory section shows a number (total memory)
mem_now=$(free -m 2>/dev/null | awk '/Mem:/{print $2}')
if echo "$OUT" | grep -Eqi "mem" && echo "$OUT" | grep -Eq "[0-9]{2,}"; then
  echo "STEP:Memory data present:PASS"
else
  echo "STEP:Memory data present:FAIL:print total memory (e.g. from free -m, host has ${mem_now}MB)"
  fail=1
fi

# Step 4 — disk section references / usage (a percentage)
if echo "$OUT" | grep -Eq "[0-9]+%"; then
  echo "STEP:Disk usage present:PASS"
else
  echo "STEP:Disk usage present:FAIL:include df -h / output (a percentage like 42%)"
  fail=1
fi

# Step 5 — --help prints usage and suppresses the dashboard
HELP=$("$SCRIPT" --help 2>/dev/null)
if echo "$HELP" | grep -qi "usage" && ! echo "$HELP" | grep -qi "hostname"; then
  echo "STEP:--help prints usage:PASS"
else
  echo "STEP:--help prints usage:FAIL:--help must print a usage line and skip the dashboard"
  fail=1
fi

exit $fail
