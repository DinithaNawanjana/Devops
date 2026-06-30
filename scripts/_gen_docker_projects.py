#!/usr/bin/env python3
"""Authoring helper: Docker project set (spec §5, projects 02-10).

Docker validators use a two-tier design:
  * STRUCTURAL checks (Dockerfile / compose / script correctness) always run —
    deterministic and testable without a daemon.
  * RUNTIME checks (build / run / curl) are guarded by `docker info`, so they
    execute in the dind lab sandbox (where Docker is always present) but are
    skipped in environments without a daemon. This is not a learner bypass:
    the real lab always has Docker.

Each project ships `_solution_cmds` (writes the reference artifacts) embedded in
solution.md and used by scripts/_test_docker_projects.sh.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "docker"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


# ── 02 Static website ────────────────────────────────────
proj(
    dir="02-static-website", id="proj-docker-static", title="Project: Containerize a Static Site",
    minutes=30, points=200, prereq="[docker-01]",
    theory="""# Project: Containerize a Static Site

Package a static website into an Nginx image. The pattern: `FROM nginx:alpine`,
then `COPY` your HTML into `/usr/share/nginx/html/`.
""",
    instructions="""# Project Tasks

In `/root/site/` build a containerized static site:

1. **`/root/site/html/index.html`** containing the text `Hello Docker`.
2. **`/root/site/Dockerfile`** that is `FROM nginx:alpine` and **COPYs** your
   `html/` into `/usr/share/nginx/html/`.

Then (in the lab terminal) build and run it:

```bash
cd /root/site
docker build -t static-site .
docker run -d --name web -p 8081:80 static-site
curl http://localhost:8081      # Hello Docker
```

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf site
mkdir -p site/html
exit 0
""",
    solution="""mkdir -p /root/site/html
echo "<h1>Hello Docker</h1>" > /root/site/html/index.html
cat > /root/site/Dockerfile <<'DF'
FROM nginx:alpine
COPY html/ /usr/share/nginx/html/
DF
""",
    validate="""#!/bin/sh
cd /root/site 2>/dev/null || { echo "STEP:site dir exists:FAIL:/root/site missing"; exit 1; }
fail=0
if grep -qi "^FROM nginx" Dockerfile 2>/dev/null; then echo "STEP:Dockerfile FROM nginx:PASS"; else echo "STEP:Dockerfile FROM nginx:FAIL:base image should be nginx"; fail=1; fi
if grep -q "usr/share/nginx/html" Dockerfile 2>/dev/null; then echo "STEP:COPY into nginx web root:PASS"; else echo "STEP:COPY into nginx web root:FAIL:COPY html into /usr/share/nginx/html/"; fail=1; fi
if grep -qi "Hello Docker" html/index.html 2>/dev/null; then echo "STEP:index.html content:PASS"; else echo "STEP:index.html content:FAIL:html/index.html should say Hello Docker"; fail=1; fi
if docker info >/dev/null 2>&1; then
  docker rm -f lab_static >/dev/null 2>&1
  if docker build -q -t lab_static . >/dev/null 2>&1 \
     && docker run -d --name lab_static -p 8081:80 lab_static >/dev/null 2>&1; then
    sleep 2
    if curl -s http://localhost:8081 | grep -qi "Hello Docker"; then echo "STEP:[runtime] site serves Hello Docker:PASS"; else echo "STEP:[runtime] site serves Hello Docker:FAIL:container did not serve the page"; fail=1; fi
  else
    echo "STEP:[runtime] image builds & runs:FAIL:docker build/run failed"; fail=1
  fi
  docker rm -f lab_static >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 03 Dockerize an app ──────────────────────────────────
proj(
    dir="03-dockerize-app", id="proj-docker-app", title="Project: Dockerize a Web App",
    minutes=40, points=250, prereq="[proj-docker-static]",
    theory="""# Project: Dockerize a Web App

Wrap an application in a Dockerfile: pick a runtime base image, `COPY` the code,
`EXPOSE` the port, and set the `CMD` that starts it.
""",
    instructions="""# Project Tasks

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
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf app
mkdir -p app
exit 0
""",
    solution="""mkdir -p /root/app
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
""",
    validate="""#!/bin/sh
cd /root/app 2>/dev/null || { echo "STEP:app dir exists:FAIL:/root/app missing"; exit 1; }
fail=0
[ -f app.py ] && echo "STEP:app.py present:PASS" || { echo "STEP:app.py present:FAIL:create app.py"; fail=1; }
grep -qi "^FROM python" Dockerfile 2>/dev/null && echo "STEP:FROM python base:PASS" || { echo "STEP:FROM python base:FAIL:base on python image"; fail=1; }
grep -qi "EXPOSE 5000" Dockerfile 2>/dev/null && echo "STEP:EXPOSE 5000:PASS" || { echo "STEP:EXPOSE 5000:FAIL:EXPOSE 5000"; fail=1; }
grep -q "app.py" Dockerfile 2>/dev/null && grep -qiE "CMD|ENTRYPOINT" Dockerfile 2>/dev/null && echo "STEP:CMD runs app.py:PASS" || { echo "STEP:CMD runs app.py:FAIL:CMD should run app.py"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker rm -f lab_app >/dev/null 2>&1
  if docker build -q -t lab_app . >/dev/null 2>&1 && docker run -d --name lab_app -p 5000:5000 lab_app >/dev/null 2>&1; then
    sleep 2
    curl -s http://localhost:5000 | grep -qi "OK from app" && echo "STEP:[runtime] app responds:PASS" || { echo "STEP:[runtime] app responds:FAIL:no OK from app"; fail=1; }
  else echo "STEP:[runtime] image builds & runs:FAIL:build/run failed"; fail=1; fi
  docker rm -f lab_app >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 04 Multi-stage optimize ──────────────────────────────
proj(
    dir="04-multistage-optimize", id="proj-docker-multistage", title="Project: Multi-stage Build",
    minutes=40, points=250, prereq="[proj-docker-app]",
    theory="""# Project: Multi-stage Build

A multi-stage Dockerfile builds artifacts in a fat "builder" stage, then copies
only the result into a slim final image — smaller, fewer CVEs.

```dockerfile
FROM golang:alpine AS builder
RUN go build -o /app ...
FROM alpine
COPY --from=builder /app /app
```
""",
    instructions="""# Project Tasks

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
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf ms
mkdir -p ms
exit 0
""",
    solution="""mkdir -p /root/ms
cat > /root/ms/Dockerfile <<'DF'
FROM alpine:3.19 AS builder
RUN mkdir -p /out && echo "built artifact" > /out/app.txt

FROM alpine:3.19
COPY --from=builder /out/app.txt /app/app.txt
CMD ["cat", "/app/app.txt"]
DF
""",
    validate="""#!/bin/sh
cd /root/ms 2>/dev/null || { echo "STEP:ms dir exists:FAIL:/root/ms missing"; exit 1; }
fail=0
froms=$(grep -ci "^FROM " Dockerfile 2>/dev/null)
[ "${froms:-0}" -ge 2 ] && echo "STEP:two or more build stages:PASS" || { echo "STEP:two or more build stages:FAIL:need >=2 FROM stages"; fail=1; }
grep -qiE "AS +builder" Dockerfile 2>/dev/null && echo "STEP:named builder stage:PASS" || { echo "STEP:named builder stage:FAIL:name the first stage 'AS builder'"; fail=1; }
grep -qi "COPY --from=" Dockerfile 2>/dev/null && echo "STEP:COPY --from between stages:PASS" || { echo "STEP:COPY --from between stages:FAIL:use COPY --from=builder"; fail=1; }
tail -n 20 Dockerfile | grep -qi "FROM alpine" && echo "STEP:final stage is alpine:PASS" || { echo "STEP:final stage is alpine:FAIL:final stage should be alpine"; fail=1; }
if docker info >/dev/null 2>&1; then
  if docker build -q -t lab_ms . >/dev/null 2>&1; then
    docker run --rm lab_ms 2>/dev/null | grep -qi "built artifact" && echo "STEP:[runtime] artifact copied & runs:PASS" || { echo "STEP:[runtime] artifact copied & runs:FAIL:output missing"; fail=1; }
  else echo "STEP:[runtime] image builds:FAIL:build failed"; fail=1; fi
  docker rmi -f lab_ms >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 05 Private registry ──────────────────────────────────
proj(
    dir="05-private-registry", id="proj-docker-registry", title="Project: Private Registry",
    minutes=45, points=300, prereq="[proj-docker-multistage]",
    theory="""# Project: Private Registry

The `registry:2` image runs your own image registry. Tag images as
`localhost:5000/<name>` and `docker push` them.
""",
    instructions="""# Project Tasks

Write `/root/registry/run.sh` that:

1. Starts a **`registry:2`** container publishing port **5000**.
2. Builds a small image and **tags it `localhost:5000/demo:1`**.
3. **Pushes** it to the local registry.

```bash
cd /root/registry
./run.sh
curl http://localhost:5000/v2/_catalog    # {"repositories":["demo"]}
```

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf registry
mkdir -p registry
exit 0
""",
    solution="""mkdir -p /root/registry
cat > /root/registry/run.sh <<'SH'
#!/bin/bash
set -e
docker rm -f registry >/dev/null 2>&1 || true
docker run -d --name registry -p 5000:5000 registry:2
printf 'FROM alpine:3.19\\nCMD ["echo","hi"]\\n' > /root/registry/Dockerfile
docker build -t localhost:5000/demo:1 /root/registry
docker push localhost:5000/demo:1
SH
chmod +x /root/registry/run.sh
""",
    validate="""#!/bin/sh
cd /root/registry 2>/dev/null || { echo "STEP:registry dir exists:FAIL:/root/registry missing"; exit 1; }
fail=0
[ -x run.sh ] && echo "STEP:run.sh is executable:PASS" || { echo "STEP:run.sh is executable:FAIL:create executable run.sh"; fail=1; }
grep -q "registry:2" run.sh 2>/dev/null && grep -q "5000" run.sh 2>/dev/null && echo "STEP:starts registry:2 on 5000:PASS" || { echo "STEP:starts registry:2 on 5000:FAIL:run registry:2 on port 5000"; fail=1; }
grep -q "push localhost:5000" run.sh 2>/dev/null && echo "STEP:pushes to localhost:5000:PASS" || { echo "STEP:pushes to localhost:5000:FAIL:docker push localhost:5000/..."; fail=1; }
if docker info >/dev/null 2>&1; then
  sh run.sh >/dev/null 2>&1
  sleep 2
  curl -s http://localhost:5000/v2/_catalog | grep -qi "demo" && echo "STEP:[runtime] image pushed to registry:PASS" || { echo "STEP:[runtime] image pushed to registry:FAIL:catalog missing demo"; fail=1; }
  docker rm -f registry >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 06 Named volumes ─────────────────────────────────────
proj(
    dir="06-named-volumes", id="proj-docker-volume", title="Project: Persistent Named Volume",
    minutes=35, points=250, prereq="[proj-docker-registry]",
    theory="""# Project: Named Volumes

Named volumes persist data independently of any container's lifecycle. Create
one with `docker volume create`, mount with `-v name:/path`.
""",
    instructions="""# Project Tasks

Write `/root/vol/run.sh` that demonstrates persistence:

1. Creates a **named volume** `labdata`.
2. Runs a container that **writes** `persisted` into a file on that volume.
3. Runs a **second** container that **reads it back** (proving the data
   survived the first container being gone).

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf vol
mkdir -p vol
exit 0
""",
    solution="""mkdir -p /root/vol
cat > /root/vol/run.sh <<'SH'
#!/bin/bash
set -e
docker volume create labdata >/dev/null
docker run --rm -v labdata:/data alpine:3.19 sh -c 'echo persisted > /data/file.txt'
docker run --rm -v labdata:/data alpine:3.19 cat /data/file.txt
SH
chmod +x /root/vol/run.sh
""",
    validate="""#!/bin/sh
cd /root/vol 2>/dev/null || { echo "STEP:vol dir exists:FAIL:/root/vol missing"; exit 1; }
fail=0
[ -x run.sh ] && echo "STEP:run.sh is executable:PASS" || { echo "STEP:run.sh is executable:FAIL:create executable run.sh"; fail=1; }
grep -q "volume create" run.sh 2>/dev/null && echo "STEP:creates a named volume:PASS" || { echo "STEP:creates a named volume:FAIL:use docker volume create"; fail=1; }
grep -qE "\\-v +labdata:" run.sh 2>/dev/null && echo "STEP:mounts the named volume:PASS" || { echo "STEP:mounts the named volume:FAIL:mount -v labdata:/data"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker volume rm labdata >/dev/null 2>&1
  sh run.sh 2>/dev/null | grep -qi "persisted" && echo "STEP:[runtime] data persists across containers:PASS" || { echo "STEP:[runtime] data persists across containers:FAIL:read-back did not show persisted"; fail=1; }
  docker volume rm labdata >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 07 Custom network ────────────────────────────────────
proj(
    dir="07-custom-network", id="proj-docker-network", title="Project: Custom Network (3 services)",
    minutes=40, points=250, prereq="[proj-docker-volume]",
    theory="""# Project: Custom Network

Services on the same user-defined network reach each other by **name**. Define a
network in Compose and attach every service to it.
""",
    instructions="""# Project Tasks

Write `/root/net/docker-compose.yml` with **three services** — `web`, `api`,
`cache` — all attached to a **custom network** named `appnet`.

- `web` and `api`: `nginx:alpine`
- `cache`: `redis:7-alpine`

```bash
cd /root/net
docker compose up -d
docker compose ps
```

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf net
mkdir -p net
exit 0
""",
    solution="""mkdir -p /root/net
cat > /root/net/docker-compose.yml <<'YML'
services:
  web:
    image: nginx:alpine
    networks: [appnet]
  api:
    image: nginx:alpine
    networks: [appnet]
  cache:
    image: redis:7-alpine
    networks: [appnet]
networks:
  appnet:
YML
""",
    validate="""#!/bin/sh
cd /root/net 2>/dev/null || { echo "STEP:net dir exists:FAIL:/root/net missing"; exit 1; }
F=docker-compose.yml
fail=0
n=$(grep -cE "^[[:space:]]+image:" "$F" 2>/dev/null)
[ "${n:-0}" -ge 3 ] && echo "STEP:three services defined:PASS" || { echo "STEP:three services defined:FAIL:need web, api, cache"; fail=1; }
grep -q "appnet" "$F" 2>/dev/null && grep -qE "^networks:" "$F" 2>/dev/null && echo "STEP:custom network appnet defined:PASS" || { echo "STEP:custom network appnet defined:FAIL:define a networks: appnet and attach services"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker compose up -d >/dev/null 2>&1
  sleep 3
  r=$(docker compose ps --status running --format '{{.Name}}' 2>/dev/null | grep -c .)
  [ "${r:-0}" -ge 3 ] && echo "STEP:[runtime] 3 services running:PASS" || { echo "STEP:[runtime] 3 services running:FAIL:found ${r:-0}"; fail=1; }
  docker compose down >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 08 Healthchecks & restart ────────────────────────────
proj(
    dir="08-healthchecks", id="proj-docker-health", title="Project: Healthchecks & Restart Policy",
    minutes=35, points=250, prereq="[proj-docker-network]",
    theory="""# Project: Healthchecks & Restart Policies

A `healthcheck` tells Docker how to probe a container's liveness; a `restart`
policy (`unless-stopped`, `always`) keeps it running across failures — the basis
of production-like resilience.
""",
    instructions="""# Project Tasks

Write `/root/health/docker-compose.yml` with a `web` service (`nginx:alpine`)
that has:

1. A **`healthcheck`** with a `test` command that probes the server.
2. A **`restart`** policy of `unless-stopped` (or `always`).

```bash
cd /root/health
docker compose up -d
docker compose ps      # shows (healthy) once probes pass
```

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf health
mkdir -p health
exit 0
""",
    solution="""mkdir -p /root/health
cat > /root/health/docker-compose.yml <<'YML'
services:
  web:
    image: nginx:alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/"]
      interval: 5s
      timeout: 3s
      retries: 3
YML
""",
    validate="""#!/bin/sh
cd /root/health 2>/dev/null || { echo "STEP:health dir exists:FAIL:/root/health missing"; exit 1; }
F=docker-compose.yml
fail=0
grep -qi "healthcheck:" "$F" 2>/dev/null && grep -qi "test:" "$F" 2>/dev/null && echo "STEP:healthcheck with a test:PASS" || { echo "STEP:healthcheck with a test:FAIL:add a healthcheck: test:"; fail=1; }
grep -qiE "restart:[[:space:]]*(unless-stopped|always)" "$F" 2>/dev/null && echo "STEP:restart policy set:PASS" || { echo "STEP:restart policy set:FAIL:add restart: unless-stopped"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker compose up -d >/dev/null 2>&1
  ok=0
  i=0
  while [ "$i" -lt 10 ]; do
    docker compose ps 2>/dev/null | grep -qi "healthy" && { ok=1; break; }
    i=$((i+1)); sleep 2
  done
  [ "$ok" = "1" ] && echo "STEP:[runtime] container reports healthy:PASS" || { echo "STEP:[runtime] container reports healthy:FAIL:never became healthy"; fail=1; }
  docker compose down >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 09 Build & push script ───────────────────────────────
proj(
    dir="09-build-push-script", id="proj-docker-buildpush", title="Project: Build & Push Script",
    minutes=40, points=300, prereq="[proj-docker-health]",
    theory="""# Project: Build & Push Automation

A reusable build/push script: parameterize the image name and version with
variables, build, tag, and push — **never** hardcode credentials.
""",
    instructions="""# Project Tasks

In `/root/cicd/` create a `Dockerfile` and a **`build.sh`** that:

1. Reads an **`IMAGE`** and a **`VERSION`** from variables (with defaults) —
   no hardcoded passwords/tokens.
2. Runs **`docker build`** tagging `"$IMAGE:$VERSION"`.
3. Runs **`docker push "$IMAGE:$VERSION"`** (default `IMAGE=localhost:5000/myapp`).

A local registry is started for you by the checker. Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf cicd
mkdir -p cicd
exit 0
""",
    solution="""mkdir -p /root/cicd
printf 'FROM alpine:3.19\\nCMD ["echo","app"]\\n' > /root/cicd/Dockerfile
cat > /root/cicd/build.sh <<'SH'
#!/bin/bash
set -euo pipefail
IMAGE="${IMAGE:-localhost:5000/myapp}"
VERSION="${VERSION:-1.0.0}"
docker build -t "$IMAGE:$VERSION" .
docker push "$IMAGE:$VERSION"
SH
chmod +x /root/cicd/build.sh
""",
    validate="""#!/bin/sh
cd /root/cicd 2>/dev/null || { echo "STEP:cicd dir exists:FAIL:/root/cicd missing"; exit 1; }
fail=0
[ -x build.sh ] && echo "STEP:build.sh is executable:PASS" || { echo "STEP:build.sh is executable:FAIL:create executable build.sh"; fail=1; }
grep -q "docker build" build.sh 2>/dev/null && grep -q "docker push" build.sh 2>/dev/null && echo "STEP:builds and pushes:PASS" || { echo "STEP:builds and pushes:FAIL:script must docker build and docker push"; fail=1; }
grep -qE "VERSION" build.sh 2>/dev/null && echo "STEP:version parameterized:PASS" || { echo "STEP:version parameterized:FAIL:use a VERSION variable"; fail=1; }
if grep -qiE "(--password|-p )[A-Za-z0-9]{4,}" build.sh 2>/dev/null; then echo "STEP:no hardcoded credentials:FAIL:remove the hardcoded password"; fail=1; else echo "STEP:no hardcoded credentials:PASS"; fi
if docker info >/dev/null 2>&1; then
  docker rm -f registry >/dev/null 2>&1
  docker run -d --name registry -p 5000:5000 registry:2 >/dev/null 2>&1
  sleep 2
  ( cd /root/cicd && sh build.sh >/dev/null 2>&1 )
  curl -s http://localhost:5000/v2/_catalog | grep -qi "myapp" && echo "STEP:[runtime] image pushed:PASS" || { echo "STEP:[runtime] image pushed:FAIL:myapp not in registry catalog"; fail=1; }
  docker rm -f registry >/dev/null 2>&1
fi
exit $fail
""",
)

# ── 10 Full-stack compose ────────────────────────────────
proj(
    dir="10-fullstack-compose", id="proj-docker-fullstack", title="Project: Full-stack Compose",
    minutes=60, points=400, prereq="[proj-docker-buildpush]",
    theory="""# Project: Full-stack with Compose

Tie a whole system together: frontend, backend, database, and a reverse proxy
in one `docker-compose.yml`, with `depends_on` ordering and published ports.
""",
    instructions="""# Project Tasks

Write `/root/full/docker-compose.yml` with **four services**:

1. `frontend` and `backend` (any image, e.g. `nginx:alpine`).
2. `db` (e.g. `redis:7-alpine`).
3. `proxy` (`nginx:alpine`) that **publishes port 8080** and `depends_on` the
   frontend and backend.

```bash
cd /root/full
docker compose up -d
curl http://localhost:8080
```

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf full
mkdir -p full
exit 0
""",
    solution="""mkdir -p /root/full
cat > /root/full/docker-compose.yml <<'YML'
services:
  frontend:
    image: nginx:alpine
  backend:
    image: nginx:alpine
  db:
    image: redis:7-alpine
  proxy:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - frontend
      - backend
YML
""",
    validate="""#!/bin/sh
cd /root/full 2>/dev/null || { echo "STEP:full dir exists:FAIL:/root/full missing"; exit 1; }
F=docker-compose.yml
fail=0
n=$(grep -cE "^[[:space:]]+image:" "$F" 2>/dev/null)
[ "${n:-0}" -ge 4 ] && echo "STEP:four services defined:PASS" || { echo "STEP:four services defined:FAIL:need frontend, backend, db, proxy"; fail=1; }
grep -qi "proxy:" "$F" 2>/dev/null && grep -q "8080" "$F" 2>/dev/null && echo "STEP:proxy publishes 8080:PASS" || { echo "STEP:proxy publishes 8080:FAIL:proxy should publish 8080"; fail=1; }
grep -qi "depends_on" "$F" 2>/dev/null && echo "STEP:depends_on ordering:PASS" || { echo "STEP:depends_on ordering:FAIL:add depends_on to the proxy"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker compose up -d >/dev/null 2>&1
  sleep 3
  code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 2>/dev/null)
  [ "$code" = "200" ] && echo "STEP:[runtime] proxy responds 200:PASS" || { echo "STEP:[runtime] proxy responds 200:FAIL:got '$code'"; fail=1; }
  docker compose down >/dev/null 2>&1
fi
exit $fail
""",
)


def write_exec(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main():
    for p in PROJECTS:
        d = BASE / p["dir"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "project.yaml").write_text(
            f"id: {p['id']}\n"
            f"title: \"{p['title']}\"\n"
            f"track: docker\nlevel: intermediate\n"
            f"estimated_minutes: {p['minutes']}\n"
            f"image: lab-docker:latest\n"
            f"prerequisites: {p['prereq']}\n"
            f"points: {p['points']}\n",
            encoding="utf-8",
        )
        (d / "theory.md").write_text(p["theory"], encoding="utf-8")
        (d / "instructions.md").write_text(p["instructions"], encoding="utf-8")
        write_exec(d / "setup.sh", p["setup"])
        write_exec(d / "validate.sh", p["validate"])
        (d / "solution.md").write_text(
            "# Solution\n\n```bash\n" + p["solution"].strip() + "\n```\n",
            encoding="utf-8",
        )
        write_exec(d / ".solution.sh", "#!/bin/bash\nset -e\n" + p["solution"])
    print(f"Wrote {len(PROJECTS)} docker projects to {BASE}")


if __name__ == "__main__":
    main()
