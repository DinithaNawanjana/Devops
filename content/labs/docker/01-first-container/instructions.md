# Your Task

The Docker daemon is running inside your sandbox. Complete these steps:

1. **Run an Nginx container**

   Start a detached Nginx container **named `web`**, publishing host port
   `8080` to container port `80`.

   ```bash
   docker run -d --name web -p 8080:80 nginx:alpine
   ```

2. **Verify it serves traffic**

   Confirm Nginx responds:

   ```bash
   curl -s http://localhost:8080 | head
   ```

3. **Create a marker file**

   Write the running container's ID into `/root/container_id.txt`:

   ```bash
   docker ps -q --filter name=web > /root/container_id.txt
   ```

Click **Check** when the `web` container is running and reachable.
