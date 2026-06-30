# Project Tasks

In `/root/app/` containerize a tiny Python web app:

1. **`/root/app/app.py`** — an HTTP server on port `5000` that responds with the
   body `OK from app` (a stdlib `http.server` is fine).
2. **`/root/app/Dockerfile`** — `FROM python:3.11-alpine`, copy `app.py`,
   `EXPOSE 5000`, and `CMD` that runs `python app.py`.

Build & run:

```bash
cd /root/app
docker build -t myapp .
docker run -d --name app -p 5000:5000 myapp
curl http://localhost:5000     # OK from app
```

Click **Check**.
