# Solution

```bash
cat > /root/fizzbuzz.sh <<'SCRIPT'
#!/bin/bash
set -euo pipefail

usage() { echo "usage: fizzbuzz.sh N"; }

classify() {
  local n="$1"
  if   (( n % 15 == 0 )); then echo "fizzbuzz"
  elif (( n % 3  == 0 )); then echo "fizz"
  elif (( n % 5  == 0 )); then echo "buzz"
  else echo "$n"
  fi
}

if [ "$#" -lt 1 ]; then
  usage
  exit 1
fi

for (( i = 1; i <= $1; i++ )); do
  classify "$i"
done
SCRIPT

chmod 755 /root/fizzbuzz.sh
./fizzbuzz.sh 15
```
