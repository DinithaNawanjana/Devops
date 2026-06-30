# Solution

```bash
# 1. Start the server in the background
cd /root/www
python3 -m http.server 8000 &
sleep 1
cd /root

# 2. Home page status -> 200
curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/ > /root/status.txt

# 3. Missing path -> 404
curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/nope > /root/missing.txt

# 4. Port open check
nc -z localhost 8000 && echo open > /root/port.txt

cat /root/status.txt /root/missing.txt /root/port.txt
# stop the server when done
pkill -f http.server
```
