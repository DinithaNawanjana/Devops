# Solution

```bash
mkdir -p /root/sec
cat > /root/sec/Dockerfile <<'DF'
FROM python:3.11-alpine
RUN adduser -D appuser
WORKDIR /app
COPY . .
USER appuser
CMD ["python", "app.py"]
DF
```
