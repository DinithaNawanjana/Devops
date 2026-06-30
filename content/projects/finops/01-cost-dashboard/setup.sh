#!/bin/sh
cd /root || exit 0
rm -rf finops
mkdir -p finops
cat > finops/bill.csv <<'CSV'
service,cost
compute,120.50
storage,30.00
database,80.00
compute,19.50
CSV
exit 0
