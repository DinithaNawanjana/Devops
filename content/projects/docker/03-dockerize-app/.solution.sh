#!/bin/bash
set -e
mkdir -p /root/app
cat > /root/app/app.py <<'PY'
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK from app")
HTTPServer(("0.0.0.0", 5000), H).serve_forever()
PY
cat > /root/app/Dockerfile <<'DF'
FROM python:3.11-alpine
WORKDIR /app
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
DF
