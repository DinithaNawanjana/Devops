#!/bin/bash
set -e
mkdir -p /root/vol
cat > /root/vol/run.sh <<'SH'
#!/bin/bash
set -e
docker volume create labdata >/dev/null
docker run --rm -v labdata:/data alpine:3.19 sh -c 'echo persisted > /data/file.txt'
docker run --rm -v labdata:/data alpine:3.19 cat /data/file.txt
SH
chmod +x /root/vol/run.sh
