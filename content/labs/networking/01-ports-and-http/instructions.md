# Your Task

`setup.sh` created `/root/www/index.html`. You'll serve it and probe it.

1. **Start a web server** on port **8000** serving `/root/www`:

   ```bash
   cd /root/www
   python3 -m http.server 8000 &        # & runs it in the background
   cd /root
   ```

2. **Capture the home-page status** — write the HTTP status code of
   `GET http://localhost:8000/` into `/root/status.txt` (should be `200`):

   ```bash
   curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/ > /root/status.txt
   ```

3. **Capture a 404** — write the status code for a missing path
   `http://localhost:8000/nope` into `/root/missing.txt`.

4. **Confirm the port is open** — using `nc`, write the word `open` into
   `/root/port.txt` if port 8000 accepts connections:

   ```bash
   nc -z localhost 8000 && echo open > /root/port.txt
   ```

Click **Check** when the four evidence files are in place.

> When you're done you can stop the server with `kill %1` or `pkill -f http.server`.
