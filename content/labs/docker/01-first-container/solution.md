# Solution

```bash
# 1. Run Nginx detached, named, with a published port
docker run -d --name web -p 8080:80 nginx:alpine

# 2. Verify
curl -s http://localhost:8080 | head

# 3. Record the container id
docker ps -q --filter name=web > /root/container_id.txt
```

Clean up afterwards with `docker rm -f web`.
