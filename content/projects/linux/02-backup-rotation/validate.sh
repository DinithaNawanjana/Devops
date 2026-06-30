#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
SCRIPT=./backup.sh

# Step 1 — executable script with shebang
if [ -f "$SCRIPT" ]; then
  mode=$(stat -c "%a" "$SCRIPT" 2>/dev/null)
  if [ "$mode" = "755" ] && head -1 "$SCRIPT" | grep -q "bin/bash"; then
    echo "STEP:Executable script with shebang:PASS"
  else
    echo "STEP:Executable script with shebang:FAIL:need mode 755 + #!/bin/bash (got $mode)"
    fail=1
  fi
else
  echo "STEP:Executable script with shebang:FAIL:/root/backup.sh missing"
  echo "STEP:Creates a valid archive:FAIL:no script"
  echo "STEP:Rotation keeps 3 newest:FAIL:no script"
  echo "STEP:Writes a log:FAIL:no script"
  exit 1
fi

# Fresh state, then run the script 5 times (sleep so timestamps differ).
rm -rf backups
i=0
while [ "$i" -lt 5 ]; do
  "$SCRIPT" >/dev/null 2>&1
  i=$((i + 1))
  sleep 1
done

# Step 2 — a valid archive exists and contains the data
newest=$(ls -1t backups/backup-*.tar.gz 2>/dev/null | head -1)
if [ -n "$newest" ] && tar tzf "$newest" >/dev/null 2>&1 \
   && tar tzf "$newest" 2>/dev/null | grep -q "app.conf"; then
  echo "STEP:Creates a valid archive:PASS"
else
  echo "STEP:Creates a valid archive:FAIL:produce backups/backup-<ts>.tar.gz of /root/data"
  fail=1
fi

# Step 3 — rotation keeps exactly 3
count=$(ls -1 backups/backup-*.tar.gz 2>/dev/null | wc -l | tr -d ' ')
if [ "$count" = "3" ]; then
  echo "STEP:Rotation keeps 3 newest:PASS"
else
  echo "STEP:Rotation keeps 3 newest:FAIL:after 5 runs expected 3 archives, found $count"
  fail=1
fi

# Step 4 — a log file was written
if [ -s backups/backup.log ]; then
  echo "STEP:Writes a log:PASS"
else
  echo "STEP:Writes a log:FAIL:append a line to backups/backup.log each run"
  fail=1
fi

exit $fail
