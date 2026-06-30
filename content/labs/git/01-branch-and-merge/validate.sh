#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:Repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0

# Step 1 — baseline commit on main with app.txt=v1
if git rev-parse --verify main >/dev/null 2>&1 \
   && git cat-file -p main:app.txt 2>/dev/null | grep -q "v1"; then
  echo "STEP:Baseline commit on main (app.txt=v1):PASS"
else
  echo "STEP:Baseline commit on main (app.txt=v1):FAIL:commit app.txt containing v1 on main"
  fail=1
fi

# Step 2 — feature branch exists
if git rev-parse --verify feature >/dev/null 2>&1; then
  echo "STEP:feature branch created:PASS"
else
  echo "STEP:feature branch created:FAIL:create a branch named feature"
  fail=1
fi

# Step 3 — feature.txt was committed on the feature branch's history
if git rev-parse --verify feature >/dev/null 2>&1 \
   && git cat-file -p feature:feature.txt 2>/dev/null | grep -q "hello feature"; then
  echo "STEP:feature.txt committed on feature:PASS"
else
  echo "STEP:feature.txt committed on feature:FAIL:commit feature.txt (hello feature) on feature"
  fail=1
fi

# Step 4 — main now contains both files (merge happened)
if git cat-file -p main:app.txt >/dev/null 2>&1 \
   && git cat-file -p main:feature.txt >/dev/null 2>&1; then
  echo "STEP:feature merged into main:PASS"
else
  echo "STEP:feature merged into main:FAIL:switch to main and merge feature"
  fail=1
fi

exit $fail
