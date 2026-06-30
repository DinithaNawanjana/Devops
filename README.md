# 🚀 DevOps Learning Platform

A self-hosted, LabEx-style interactive learning platform for DevOps. Runs
locally. Every topic combines **theory + hands-on browser labs + projects**,
each with an auto-validation checker.

> Move from **Beginner → Expert**: Linux, Bash, Git, Docker, CI/CD, Ansible,
> Terraform, Kubernetes, monitoring, DevSecOps, GitOps, SRE and more.

---

## What's in this repo

```
.
├── docker-compose.yml      # full local stack (web + api + db + redis)
├── backend/                # FastAPI API + lab engine (Docker SDK)
│   └── app/
│       ├── routers/        # auth, catalog, labs, progress
│       └── lab_engine/     # session manager, terminal bridge, validation
├── frontend/               # Next.js + Tailwind (xterm.js terminal, Monaco)
├── content/                # all course content as git-versionable files
│   ├── tracks/<slug>/track.yaml
│   └── labs/<track>/<slug>/{lab.yaml,theory.md,instructions.md,
│                            setup.sh,validate.sh,solution.md}
├── lab-images/             # sandbox base images (lab-linux, lab-docker/dind)
└── scripts/                # helpers (build images, generate tracks)
```

This corresponds to **Phase 1 (skeleton)** + **Phase 2 (the lab engine)** of
the build roadmap, plus the **content pipeline** and three fully working
sample labs.

---

## Quick start

Requires Docker + Docker Compose.

```bash
# 1. Configure
cp .env.example .env            # edit JWT_SECRET etc. for anything real

# 2. Build the lab sandbox images (one-time)
./scripts/build-lab-images.sh

# 3. Launch the platform
docker compose up --build
```

Then open:

- **Web app:** http://localhost:3000
- **API docs:** http://localhost:8000/docs

Register an account, pick a track, open a lab, click **▶ Start Lab**, work in
the in-browser terminal, then hit **✓ Check**.

---

## How the lab engine works

1. `POST /labs/{id}/start` — the session manager creates a sandbox container
   from the lab's image (with memory/CPU/PID caps), seeds `setup.sh` +
   `validate.sh` into `/lab`, and runs setup.
2. `WS /labs/sessions/{id}/terminal?token=…` — a WebSocket bridge `exec`s
   `/bin/bash` in the container and pipes it to xterm.js in the browser.
3. `POST /labs/sessions/{id}/check` — runs `/lab/validate.sh` inside the
   container; output is parsed into per-step pass/fail and XP is awarded.
4. An idle reaper tears down containers past the idle timeout / max duration,
   and orphaned sandboxes are cleaned up on API startup.

### The lab definition format

One folder per lab under `content/labs/<track>/<slug>/`:

| File              | Purpose                                             |
|-------------------|-----------------------------------------------------|
| `lab.yaml`        | metadata (id, title, level, image, points, prereqs) |
| `theory.md`       | the lesson                                           |
| `instructions.md` | step-by-step task                                    |
| `setup.sh`        | runs on container start (seed files, clean slate)    |
| `validate.sh`     | the checker (see contract below)                     |
| `solution.md`     | revealed after completion                            |

**`validate.sh` contract** — print one line per check and exit `0` only if all
pass:

```
STEP:<name>:PASS
STEP:<name>:FAIL
STEP:<name>:FAIL:<human-readable hint>
```

Score awarded = `points × (passed steps / total steps)`.

Adding content needs **no database changes** — drop a folder and call
`POST /content/reload` (or restart the API). Content is bind-mounted read-only.

---

## Curriculum

26 tracks across four levels are pre-registered (`content/tracks/`). Three
labs are authored end-to-end as working references:

- `linux/01-filesystem-basics` — files, permissions (`lab-linux`)
- `bash/01-pipes-and-filters` — pipes, grep/awk/sort (`lab-linux`)
- `docker/01-first-container` — run Nginx in a container (`lab-docker`/dind)

Author the rest by following the same folder format. See the master spec for
the full topic + project lists.

---

## Security notes (read before exposing this)

- The API mounts the host Docker socket (`/var/run/docker.sock`) to spawn
  sandboxes. **This is privileged.** For a hardened setup use
  [Sysbox](https://github.com/nestybox/sysbox) or rootless Docker.
- Sandboxes run with `--cap-drop ALL` and `--no-new-privileges` by default.
  The Docker-in-Docker image (`lab-docker`) needs these relaxed (privileged /
  Sysbox) to run a nested daemon — wire that per-image before enabling it in
  production.
- Containers get hard `--memory`, `--cpus`, and `--pids-limit` caps
  (configurable via `.env`).
- This is a learning/dev setup. Change `JWT_SECRET`, add TLS, and put the API
  behind auth/rate limiting before any shared deployment.

---

## Local development (without Docker)

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# point DATABASE_URL/REDIS_URL at local services, then:
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

## Roadmap (remaining)

- **Phase 3:** Monaco file persistence into the sandbox; author Linux/Git/
  Docker tracks fully (theory + 10 projects each).
- **Phase 4:** Prerequisite skill tree, badges/streaks, project workspace,
  auto-grading, "Export to GitHub".
- **Phase 5:** K8s (kind/k3d) labs, monitoring/DevSecOps tracks, certificates,
  leaderboard, analytics, dark mode.
