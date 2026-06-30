#!/usr/bin/env python3
"""Deep-dive theory for the Git and Docker project tracks (teacher-style).
Same contract as enrich_theory.py: rewrites theory.md only.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROOT = ROOT / "content" / "projects"
THEORY: dict[str, str] = {}


def add(p, b): THEORY[p] = b.strip() + "\n"


# ───────────────────────────── GIT ─────────────────────────────
add("git/01-repo-setup", """
# Deep Dive: Repository Hygiene

## A repo is a contract
The first commits set the tone for everyone who joins later. A well-formed repo
declares three things up front: **what to ignore**, **what the project is**, and
**how branches are used**.

## .gitignore — keep the repo clean
Git tracks everything you `add`, so a `.gitignore` is how you keep build
artifacts, dependencies (`node_modules/`), secrets, and logs out of history.
Once a file is committed, ignoring it later does **not** remove it — you must
`git rm --cached`. Patterns are gitignore-glob: `*.log`, `dir/`, `!keep.me` to
re-include.

## README — the front door
The README is the first thing a human (and now an LLM) reads. Minimum: what the
project does, how to run it, how to contribute.

## A branching model
Even a one-line policy ("`main` is always deployable; work on `develop`/feature
branches") prevents chaos. It's the seed of Git Flow, GitHub Flow, and
trunk-based development.

## Pitfalls
- Committing secrets before adding `.gitignore` — they live in history forever
  (use `git filter-repo`/BFG to purge).
- A `main` that isn't deployable, so nobody trusts it.

## Real-world
Every repo template, `npm init`, and `gh repo create` scaffolds exactly these
files for exactly these reasons.
""")

add("git/02-merge-conflict", """
# Deep Dive: How Merges (and Conflicts) Work

## What a merge really is
A merge combines two lines of history. Git finds the **merge base** (the common
ancestor), then applies both sides' changes. If the two sides changed
*different* regions, Git merges automatically. If they changed the **same
lines**, Git can't choose — that's a conflict, and it asks you.

## Reading the markers
```
<<<<<<< HEAD
your side
=======
their side
>>>>>>> feature
```
Everything between `<<<` and `===` is the current branch; between `===` and
`>>>` is the branch being merged. Resolving = editing the file to the final
desired content and **removing all markers**, then `git add` + `git commit`.

## Fast-forward vs. merge commit
If your branch hasn't moved, Git just slides the pointer forward (fast-forward,
no new commit). If both moved, Git records a **merge commit** with *two
parents* — visible as a fork-and-join in the graph.

## Pitfalls
- Committing with conflict markers still in the file (tests/CI catch this).
- `git checkout --theirs/--ours` blindly, discarding real work.
- Resolving the same conflict repeatedly across rebases — enable `git rerere`.

## Real-world
Every pull request that "has conflicts" lands you here; mastering it is daily
bread on any team.
""")

add("git/03-pre-commit-hook", """
# Deep Dive: Git Hooks

## Shifting feedback left
A bug caught at commit time costs seconds; the same bug caught in CI costs
minutes; in production, hours. **Hooks** are scripts Git runs at lifecycle
points so you can catch problems at the earliest possible moment.

## Where hooks live
`.git/hooks/` holds them. `pre-commit` runs *before* the commit is created — exit
non-zero and the commit is **aborted**. Other useful ones: `commit-msg`
(enforce message format), `pre-push` (run tests before sharing).

## Anatomy
```sh
#!/bin/sh
if git diff --cached | grep -q "TODO"; then
  echo "blocked: remove TODOs"; exit 1
fi
```
`git diff --cached` is the **staged** content — exactly what's about to be
committed. That's what you lint.

## The catch: hooks aren't shared
`.git/hooks/` is **not** part of the repo, so teammates don't get your hook
automatically. Real teams use a manager (the `pre-commit` framework, Husky) that
installs hooks from a committed config.

## Pitfalls
- Hooks that are slow make people `--no-verify` and bypass them.
- Forgetting `chmod +x` — a non-executable hook is silently skipped.

## Real-world
Linters, formatters (Prettier/Black), secret scanners, and conventional-commit
checks all run as hooks before CI ever sees the code.
""")

add("git/04-git-flow", """
# Deep Dive: Branching Strategies

## Why a model at all
Branches are cheap; *coordination* is not. A branching model is a shared
agreement about where work happens and how it reaches production, so people
don't step on each other.

## The feature-branch flow
- `main` — always releasable.
- `develop` — integration branch where features land.
- `feature/*` — one branch per unit of work, branched off `develop`, merged
  back when done.

Merging with **`--no-ff`** forces a merge commit even when a fast-forward was
possible, preserving the feature boundary in history (you can see where a
feature began and ended).

## The spectrum
- **Git Flow**: develop + release + hotfix branches — heavy, good for versioned
  releases.
- **GitHub Flow**: just `main` + short-lived feature branches + PRs — light,
  good for continuous deployment.
- **Trunk-based**: commit to `main` behind feature flags — fastest, needs strong
  CI.

## Pitfalls
- Long-lived feature branches → merge hell. Integrate often.
- Choosing a heavy model for a tiny team.

## Real-world
The model you pick shapes your whole CI/CD pipeline; most modern teams trend
toward GitHub Flow or trunk-based.
""")

add("git/05-squash-history", """
# Deep Dive: Rewriting History Cleanly

## Two audiences for history
While you work, commits are a *save button* ("wip", "fix typo"). When you share,
history is *documentation* for reviewers and future debuggers. Squashing turns
the former into the latter.

## Two ways to squash
1. **Interactive rebase**: `git rebase -i HEAD~3`, mark commits `squash`/`fixup`.
   Full control, can reorder/reword.
2. **Soft reset**: `git reset --soft HEAD~3 && git commit`. Moves the branch
   pointer back 3 commits but **keeps the index/working tree**, so one new commit
   captures all the changes. Simpler when you just want "combine the last N".

The working tree is identical either way — only the commit graph changes.

## The golden rule
**Never rewrite history that others have pulled.** Rewriting changes commit
hashes; collaborators who based work on the old hashes get a divergent mess.
Squash *before* pushing, or only on branches you own.

## Pitfalls
- Force-pushing a rewritten shared branch (`--force-with-lease` is safer than
  `--force`, but communication is safest).
- Squashing away a commit you needed to revert independently.

## Real-world
"Squash and merge" is a one-click button on GitHub PRs precisely because clean,
atomic commits make `git bisect`, `revert`, and code archaeology sane.
""")

add("git/06-remote-push", """
# Deep Dive: Remotes & the Distributed Model

## Distributed, not centralized
Every clone is a **full repository** with all history — there's no privileged
"server" in Git's design, only repos that agree to sync. A **remote** is just a
named URL of another repo (`origin` by convention).

## Bare repos
A **bare** repo (`git init --bare`) has no working tree — it's storage only.
That's why servers (and this lab's `remote.git`) are bare: you can't push to a
branch that's checked out in a working tree, but a bare repo has none.

## Push mechanics
`git push origin feature` uploads your `feature` commits and updates the
remote's `refs/heads/feature`. Tracking (`-u`) links your local branch to the
remote one so later `git push`/`pull` need no arguments.

## Pitfalls
- Pushing to a non-bare repo's checked-out branch → rejected.
- Diverged histories → push rejected ("fetch first"); resolve with pull/rebase.
- Force-pushing over a teammate's commits.

## Real-world
This is the foundation of the fork-and-pull-request workflow that powers all of
open source: fork (a server-side clone), push a branch, open a PR.
""")

add("git/07-semver-tags", """
# Deep Dive: Tagging & Semantic Versioning

## Lightweight vs. annotated tags
- **Lightweight**: just a pointer to a commit (a named bookmark).
- **Annotated** (`git tag -a`): a real Git object with a message, tagger, and
  date — and can be GPG-signed. **Releases should always be annotated** so the
  tag carries provenance.

## Semantic Versioning
`MAJOR.MINOR.PATCH`:
- **MAJOR** — breaking changes.
- **MINOR** — new, backward-compatible features.
- **PATCH** — backward-compatible bug fixes.

This contract lets dependents pin ranges (`^1.4.0`) and know what upgrading
risks. `git describe --tags` names any commit relative to the nearest tag
(`v1.1.0-3-gabc123` = 3 commits past v1.1.0).

## Pitfalls
- Lightweight tags for releases — no metadata, easy to clobber.
- Forgetting `git push --tags` (tags don't push with commits by default).
- Re-tagging an existing version — breaks anyone who pinned it.

## Real-world
CI release pipelines trigger on tag pushes; package registries (npm, PyPI,
container registries) key releases on SemVer tags.
""")

add("git/08-reflog-recovery", """
# Deep Dive: The Reflog — Git's Safety Net

## "Lost" almost never means lost
Git rarely deletes commits immediately. When you `reset --hard`, rebase, or
delete a branch, the commits become **unreferenced** (no branch points at them),
but they survive in the object database until garbage collection runs (default
~30 days for unreachable objects).

## The reflog
`git reflog` is a local journal of **everywhere HEAD has been** — every commit,
checkout, reset, and rebase, with entries like `HEAD@{2}`. It's how you find the
hash of a commit no branch points to anymore:
```bash
git reflog                       # find the lost commit's hash
git checkout <hash> -- file      # restore a file, or
git branch rescue <hash>         # recreate a branch at it
```

## Why it's local-only
The reflog is per-clone and never pushed — it reflects *your* HEAD's journey. So
recovery is something you do in the repo where the loss happened.

## Pitfalls
- Waiting too long — `git gc` eventually prunes truly unreachable objects.
- Confusing `reflog` (HEAD movements) with `log` (commit ancestry).

## Real-world
"I rebased and lost my work" is a daily Slack message; the reflog is the calm
answer. It's also how you undo a bad `reset --hard`.
""")

add("git/09-submodules", """
# Deep Dive: Submodules & Vendoring

## The problem they solve
Sometimes a repo needs another repo inside it — a shared library, a theme, a
vendored dependency — pinned to a **specific commit**, not just "latest". A
submodule embeds repo B inside repo A at a fixed SHA.

## How they're recorded
`git submodule add <url> <path>` does three things: clones B into `path`, writes
a `.gitmodules` file (the URL + path mapping), and stages a special **gitlink**
entry that records B's exact commit. Cloning A later needs
`git submodule update --init` to populate the submodule.

## The trade-off
Submodules give **reproducibility** (exact pinned commit) but add friction:
contributors must know the extra commands, and updating the pin is a manual
commit in A. Alternatives: subtree merges, or a package manager.

## Pitfalls
- Cloning without `--recurse-submodules` → empty submodule directories.
- Forgetting to commit the updated gitlink after changing the submodule.
- The local-path/file-protocol restriction (`protocol.file.allow`) on recent
  Git for security.

## Real-world
Used for shared CI config, design systems, firmware blobs, and any "pin an exact
upstream commit" need.
""")

add("git/10-changelog", """
# Deep Dive: Changelogs from Commit History

## Why automate it
A changelog answers "what changed between releases?" for users and operators.
Hand-maintained changelogs rot; generating from commit messages keeps them
honest — and *forces* good commit hygiene.

## Conventional Commits
A lightweight convention: `type(scope): subject`, e.g. `feat: add login`,
`fix: correct typo`. Because the type is machine-readable, tools can:
- group changes into Features / Fixes / Breaking,
- auto-pick the next SemVer bump (`feat` → minor, `fix` → patch, `!`/`BREAKING
  CHANGE` → major).

## The generation
At its simplest:
```bash
git log --pretty='- %s' v1.0.0..HEAD
```
emits a bullet per commit since the last tag. `%s` is the subject; the
`tag..HEAD` range scopes it to the unreleased commits.

## Pitfalls
- Garbage in, garbage out — vague commit subjects make a useless changelog
  (this is *why* teams enforce Conventional Commits via a commit-msg hook).
- Including merge commits as noise (`--no-merges`).

## Real-world
`semantic-release`, `release-please`, and GitHub's auto-generated release notes
all build on exactly this commit-message-to-changelog pipeline.
""")

# ──────────────────────────── DOCKER ────────────────────────────
add("docker/01-compose-stack", """
# Deep Dive: Multi-container Apps with Compose

## Why Compose exists
A real app is several processes — web, database, cache. Running each with a long
`docker run` line is error-prone and undocumented. **Compose** declares the whole
topology in one `docker-compose.yml`, version-controlled and reproducible:
`docker compose up` brings it all up.

## The mental model
Each `service` becomes one (or more) containers. Compose automatically creates a
**shared network** for the project, and — crucially — services reach each other
by **service name** as a DNS hostname (`web` can connect to `cache` at host
`cache`). No IPs, no links.

## Key fields
- `image` / `build` — where the container comes from.
- `ports: "8080:80"` — publish host:container (only needed for things you reach
  from outside).
- `depends_on` — start ordering (but *not* readiness — see pitfalls).
- `environment`, `volumes`, `networks`.

## Pitfalls
- `depends_on` waits for the container to **start**, not for the app inside to be
  **ready**. Use healthchecks + `condition: service_healthy` for true readiness.
- Publishing ports you don't need (DB on the host) — an attack surface.

## Real-world
Compose runs local dev environments, CI test stacks, and many small production
deployments; its model directly informs Kubernetes pods and services.
""")

add("docker/02-static-website", """
# Deep Dive: Images, Layers & the Build Cache

## What an image is
An image is a **stack of read-only layers** plus metadata (entrypoint, env,
ports). Each Dockerfile instruction (`FROM`, `COPY`, `RUN`) creates one layer.
At run time Docker adds a thin writable layer on top — that's your container.

## Why layer order matters
Docker **caches** layers: if an instruction and everything before it is
unchanged, it reuses the cache. So put rarely-changing steps first (install
deps) and frequently-changing steps last (copy source). Get this backwards and
every code change rebuilds everything.

## This project's pattern
`FROM nginx:alpine` gives you a production web server; `COPY html/ →
/usr/share/nginx/html/` lays your site on top. The base image already knows how
to start nginx, so you write almost nothing.

## Pitfalls
- `COPY . .` invalidating the cache on every change because you copied
  everything (use a `.dockerignore`).
- Editing files in a running container — changes vanish when it's recreated;
  images are immutable, rebuild instead.
- Using `:latest` — non-reproducible builds; pin tags.

## Real-world
This is how static sites, SPAs, and documentation get shipped — build artifacts
baked into an nginx image and rolled out behind a CDN or ingress.
""")

add("docker/03-dockerize-app", """
# Deep Dive: Writing a Good Application Dockerfile

## The job of a Dockerfile
Turn source code into a self-contained, runnable image: choose a base runtime,
install dependencies, copy code, declare the port, and define the start command.

## Instruction essentials
- `FROM python:3.11-alpine` — a minimal runtime base.
- `WORKDIR /app` — sets (and creates) the working directory.
- `COPY` — dependencies first (`requirements.txt`), then code, to exploit the
  layer cache.
- `EXPOSE 5000` — **documentation** of the listening port (it doesn't publish;
  `-p` does).
- `CMD ["python","app.py"]` — the default process. Exec-form (JSON array) runs
  without a shell, so signals (SIGTERM) reach your app for clean shutdown.

## CMD vs ENTRYPOINT
`CMD` is the default command (easily overridden); `ENTRYPOINT` is the fixed
executable with `CMD` as its default args. Use ENTRYPOINT for "this image *is* a
tool".

## Pitfalls
- Shell-form `CMD python app.py` wraps your app in `/bin/sh`, which swallows
  signals → slow/forced kills.
- Running as root (add a non-root `USER`).
- Copying the whole context without `.dockerignore` (slow, leaks secrets).

## Real-world
Every microservice ships as an image built from a Dockerfile like this; the
quality of the Dockerfile decides your image size, build speed, and security.
""")

add("docker/04-multistage-optimize", """
# Deep Dive: Multi-stage Builds

## The fat-image problem
If you build *and* run in the same image, the final artifact carries compilers,
headers, dev dependencies, and build caches — bloating size and CVE surface. A
Go binary that's 10 MB can ship in a 900 MB image if you're careless.

## How multi-stage fixes it
Use several `FROM` stages in one Dockerfile. Earlier stages build; the final
stage starts from a slim base and `COPY --from=<stage>` only the finished
artifact. Build tools never reach the final image.
```dockerfile
FROM golang:alpine AS builder
RUN go build -o /app
FROM alpine          # or scratch / distroless
COPY --from=builder /app /app
```

## How small can you go
- `alpine` — ~5 MB, has a shell/package manager.
- `distroless` — no shell, just your app + runtime; smaller attack surface.
- `scratch` — empty; only works for fully static binaries.

## Pitfalls
- Copying more than the artifact (defeats the purpose).
- A `scratch`/distroless image with a dynamically-linked binary → "not found"
  at runtime (missing libc).
- Forgetting CA certs/timezone data that the slim base lacks.

## Real-world
Standard practice for compiled languages and even Node/Python (build deps in one
stage, runtime-only in the next); smaller images deploy and scale faster.
""")

add("docker/05-private-registry", """
# Deep Dive: Registries & Image Distribution

## What a registry is
A registry stores and serves images by `name:tag`. Docker Hub is the public one;
`registry:2` is the open-source server you can run yourself for private or
air-gapped use. Pushing/pulling is just HTTP against a documented API
(`/v2/...`).

## Names encode the registry
`localhost:5000/demo:1` means *host* `localhost:5000`, *repo* `demo`, *tag* `1`.
The hostname prefix is how the client knows which registry to talk to; with no
prefix, Docker defaults to Docker Hub.

## The push flow
`docker tag` gives the image a name pointing at your registry, then
`docker push` uploads each **layer** (deduplicated — shared layers upload once).
`curl http://localhost:5000/v2/_catalog` lists what's stored.

## Pitfalls
- HTTP registries are "insecure" to Docker — you must add them to
  `insecure-registries` or use TLS.
- No auth/garbage-collection by default — fine for a lab, not for production.
- Forgetting that the tag is part of the identity (`demo` ≠ `demo:1`).

## Real-world
Every team runs or rents a registry (ECR, GCR, Harbor, GitHub Packages); it's
the handoff point between CI (which builds/pushes) and CD (which pulls/deploys).
""")

add("docker/06-named-volumes", """
# Deep Dive: Persistence & Storage

## Containers are ephemeral
A container's writable layer dies with it. Anything you want to **outlive** the
container — database files, uploads — must live on a volume.

## Volumes vs. bind mounts
- **Named volume** (`docker volume create data`, `-v data:/var/lib/...`): Docker
  manages the storage location; portable, the right default for data.
- **Bind mount** (`-v /host/path:/in/container`): maps a host directory in;
  great for live-reloading source in dev, but ties you to the host layout.

## Why the lifecycle decoupling matters
You can destroy and recreate the container (upgrade the image, change flags) and
re-attach the same named volume — the data is untouched. That's what makes
stateful containers (databases) viable.

## Pitfalls
- Writing data into the container filesystem instead of the volume → lost on
  recreate.
- Two containers writing the same volume without coordination → corruption (most
  databases assume single-writer).
- Forgetting volumes persist after `docker rm` — `docker volume prune` to clean.

## Real-world
Postgres/MySQL containers, upload stores, and CI caches all rely on volumes; in
Kubernetes the same idea becomes PersistentVolumes/PVCs.
""")

add("docker/07-custom-network", """
# Deep Dive: Container Networking & Service Discovery

## The default isn't enough
On the default bridge, containers can talk by IP but **not by name**. The moment
you have more than one service, you want a **user-defined network**, which adds
an embedded DNS so containers resolve each other by **name**.

## How discovery works
On a user-defined network (which Compose creates for you), service `web` can
`curl http://api` and Docker's DNS resolves `api` to that container's current
IP — even across restarts when the IP changes. This is why you never hardcode
container IPs.

## Segmentation
Multiple networks let you isolate tiers: put the database on a `backend` network
the frontend can't reach, exposing only what's necessary. Least privilege at the
network layer.

## Pitfalls
- Relying on the default bridge and wondering why name resolution fails.
- Publishing internal services to the host (`-p`) when only other containers
  need them.
- Assuming containers on *different* networks can talk — they can't unless
  attached to a common one.

## Real-world
This DNS-by-name model is exactly how Kubernetes Services work; learning it in
Compose makes K8s networking click.
""")

add("docker/08-healthchecks", """
# Deep Dive: Healthchecks & Restart Policies

## "Running" is not "healthy"
A container's process can be up while the app inside is deadlocked, still
booting, or out of connections. A **healthcheck** is a command Docker runs
periodically *inside* the container to test real behaviour, flipping its status
between `starting`, `healthy`, and `unhealthy`.

## Defining one
```yaml
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost/"]
  interval: 5s
  timeout: 3s
  retries: 3
  start_period: 10s
```
`start_period` gives slow-booting apps grace before failures count.

## Restart policies
`restart: unless-stopped` (or `always`) tells Docker to bring a crashed
container back. Combined with healthchecks and `depends_on:
condition: service_healthy`, you get dependency ordering that waits for real
readiness, not just process start.

## Pitfalls
- A healthcheck that always passes (e.g. checking the process, not the endpoint).
- Too-aggressive intervals hammering the app.
- `restart: always` masking a crash loop instead of fixing the cause.

## Real-world
This is the Compose-level version of Kubernetes liveness/readiness probes and
the foundation of zero-downtime rollouts.
""")

add("docker/09-build-push-script", """
# Deep Dive: Build/Push Automation & Secret Hygiene

## Parameterize everything
A reusable build script never hardcodes the image name, version, or — above all
— credentials. Drive them from variables/env with sane defaults:
```bash
IMAGE="${IMAGE:-localhost:5000/myapp}"
VERSION="${VERSION:-$(git describe --tags --always)}"
docker build -t "$IMAGE:$VERSION" .
docker push  "$IMAGE:$VERSION"
```
Deriving `VERSION` from Git ties every image back to a commit — traceability.

## Credentials, the right way
Never put a password in the script or `docker login -p hunter2`. Inject at
runtime and pipe via stdin:
```bash
echo "$REGISTRY_TOKEN" | docker login -u ci --password-stdin
```
`--password-stdin` keeps the secret out of the process list and shell history;
the token comes from the CI secret store, not the repo.

## Pitfalls
- `-p <password>` on the command line — visible in `ps` and CI logs.
- Tagging only `:latest` — you can't roll back to a specific build.
- Building without a `.dockerignore` — leaks `.env`/`.git` into the image.

## Real-world
This script *is* the build stage of a CI pipeline; the only change in CI is that
the variables come from the runner's secret store.
""")

add("docker/10-fullstack-compose", """
# Deep Dive: Composing a Whole System

## From containers to architecture
This capstone of the Docker track wires four roles — frontend, backend, database,
and a reverse proxy — into one declarative stack. It's where Compose stops being
"run a container" and becomes "describe a system".

## The reverse proxy pattern
A proxy (nginx/Traefik/Caddy) is the single published entrypoint (`:8080`). It
routes paths/hosts to internal services that are **not** published to the host.
Benefits: one TLS termination point, path-based routing, and a smaller attack
surface (only the proxy is exposed).

## Ordering vs. readiness
`depends_on` sequences startup, but apps should still **retry** their
dependencies — a backend must tolerate the DB not accepting connections for the
first second. Healthchecks + `condition: service_healthy` tighten this.

## Pitfalls
- Publishing the DB/backend ports to the host "for debugging" and forgetting.
- Assuming start order equals ready order.
- One giant compose file with no profiles — split dev/prod concerns.

## Real-world
This four-tier shape (proxy → frontend/backend → datastore) is the canonical web
architecture; translating it to Kubernetes is Ingress → Services/Deployments →
StatefulSet, the same picture with cluster-grade primitives.
""")


def main():
    n = 0
    for rel, body in THEORY.items():
        t = PROOT / rel / "theory.md"
        if not t.parent.exists():
            print("  !! missing:", rel); continue
        t.write_text(body, encoding="utf-8"); n += 1
    print(f"Enriched {n} theory.md files (git + docker)")


if __name__ == "__main__":
    main()
