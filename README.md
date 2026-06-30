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

### Implemented features

**Core engine & MVP**
- JWT auth (register / login), per-user progress
- Disk-based catalog: tracks, labs, **projects**
- Lab engine: Docker session manager (CPU/mem/PID caps, idle reaper, orphan
  cleanup), xterm.js WebSocket terminal, `validate.sh` runner + Check button
- **Monaco code editor** with an in-sandbox file browser — edits save straight
  into the running container so `validate.sh` sees them
- **Reveal solution** (after attempt)

**Learning layer**
- **Prerequisite skill tree** — items show `locked / available / completed`
  per user, unlocking as prerequisites are met
- **XP, levels, daily streaks**
- **Badges** (11 definitions, auto-awarded on completion)
- **Search** across labs & projects, **dark mode**

This covers **Phase 1–2** (skeleton + lab engine) and most of **Phase 3–4**
(content pipeline, editor, progress/XP/badges/skill tree). See the roadmap at
the bottom for what remains (mostly authoring the full content library).

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

26 tracks across four levels are pre-registered (`content/tracks/`).
**108 content items** are authored — **8 labs + 100 projects** — and **every
single one ships a tested `validate.sh`**.

**Labs** (`content/labs/`) — one per beginner track + Docker
- `linux`, `bash`, `shell-scripting`, `networking`, `git`, `python-devops`,
  `cloud-concepts`, `docker`

**Projects** (`content/projects/`) — all 10 spec §5 sets, 10 each:

| Set | Track(s) | Highlights |
|-----|----------|-----------|
| Linux & Bash | `linux` | sysinfo, backup+rotation, log-analyzer, user-mgr, watcher… |
| Git | `git` | branch/merge, hooks, rebase/squash, reflog recovery, submodules |
| Docker | `docker` | static site, multi-stage, registry, volumes, networks, compose |
| CI/CD | `cicd` | Actions, Jenkins, GitLab CI, matrix, secrets, blue-green |
| Ansible | `ansible` | playbooks, roles, Jinja2, Vault, handlers, hardening |
| Terraform | `terraform` | providers, modules, backends, workspaces, count/for_each |
| Kubernetes | `kubernetes` | Pods→Ingress→HPA, Helm, RBAC, ArgoCD GitOps |
| Monitoring | `monitoring` | Prometheus, Grafana, Loki, ELK, SLO burn-rate, tracing |
| DevSecOps | `devsecops` | Trivy, Semgrep, gitleaks, Vault, cosign, OPA, NetworkPolicy |
| Capstones | `gitops`/`sre`/`finops`/… | mesh, chaos, IDP, multi-cluster, mega-platform |

The capstones are spread across the **expert tracks** (gitops, service-mesh,
chaos-engineering, sre, platform-engineering, kubernetes-advanced,
advanced-cicd, finops) so those light up too.

**Every validator is automatically tested against a reference solution.** Run:

```bash
scripts/_test_linux_projects.sh      # runnable bash projects
scripts/_test_git_projects.sh        # git end-state checks
scripts/_test_docker_projects.sh     # structural (runtime steps run in dind)
scripts/_test_cicd_projects.sh
scripts/_test_track_projects.sh <track>   # ansible|terraform|kubernetes|…
```

Validators come in two flavours: **runnable** (the validator executes the
learner's scripts — Linux, Git, FinOps, DR, blue-green, …) and **structural +
runtime-guarded** (config/manifest correctness always graded; build/run steps
run in the dind/cluster sandbox). Author more by dropping folders under
`content/labs/` or `content/projects/` — no DB changes needed.

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

Done: the platform/engine and the learning layer (editor, skill tree, XP,
streaks, badges, search, dark mode). What's left is mostly **content volume**
and a few advanced features:

- **Content library:** author the remaining labs + 10 projects per track across
  all 26 topics (the format and tooling are in place — it's authoring work).
- **Projects extras:** "Export to GitHub" button, project gallery.
- **Phase 5:** K8s (kind/k3d) labs, monitoring/DevSecOps tracks, certificates
  (PDF), leaderboard, usage analytics, AI hint assistant.
- **Hardening:** Alembic migrations, per-image security profiles for dind,
  rate limiting, tests in CI.
