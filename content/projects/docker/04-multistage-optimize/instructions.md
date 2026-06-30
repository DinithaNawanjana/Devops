# Project Tasks

Write `/root/ms/Dockerfile` as a **multi-stage** build:

1. A first stage named `builder` (use `AS builder`) that produces an artifact.
2. A final stage based on **alpine** that uses **`COPY --from=builder`** to pull
   only the artifact in.

Build it and confirm it runs:

```bash
cd /root/ms
docker build -t multistage .
docker run --rm multistage
```

Click **Check**.
