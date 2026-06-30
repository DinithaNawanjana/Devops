#!/usr/bin/env python3
"""Authoring helper: CI/CD project set (spec §5). Pipeline-file authoring,
graded structurally (deterministic, no CI engine needed); project 10 is a
runnable blue-green switch script. Standard folder format + reference solution.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "cicd"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


# ── 01 lint+test on push ─────────────────────────────────
proj(
    dir="01-gh-lint-test", id="proj-cicd-lint", title="Project: GitHub Actions Lint + Test",
    minutes=35, points=250, prereq="[docker-01]",
    theory="""# Project: Lint + Test on Every Push

A GitHub Actions workflow lives in `.github/workflows/*.yml`. It declares **when**
it runs (`on:`), and **what** to do (`jobs:` → `steps:`).
""",
    instructions="""# Project Tasks

Create `/root/repo/.github/workflows/ci.yml`:

1. Trigger **`on: push`** (pull_request too is nice).
2. A job with **`runs-on: ubuntu-latest`**.
3. Steps that **lint and test** (e.g. `run: flake8 .` and `run: pytest`).

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo/.github/workflows
exit 0
""",
    solution="""mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/ci.yml <<'YML'
name: CI
on:
  push:
  pull_request:
jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: flake8 .
      - name: Test
        run: pytest -q
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.github/workflows/ci.yml
fail=0
[ -f "$F" ] && echo "STEP:ci.yml exists:PASS" || { echo "STEP:ci.yml exists:FAIL:create .github/workflows/ci.yml"; exit 1; }
grep -qE "^on:|push" "$F" && echo "STEP:triggers on push:PASS" || { echo "STEP:triggers on push:FAIL:add on: push"; fail=1; }
grep -q "runs-on:" "$F" && echo "STEP:job runs-on defined:PASS" || { echo "STEP:job runs-on defined:FAIL:add runs-on"; fail=1; }
grep -q "run:" "$F" && echo "STEP:runs lint/test steps:PASS" || { echo "STEP:runs lint/test steps:FAIL:add run: steps"; fail=1; }
exit $fail
""",
)

# ── 02 build+push on tag ─────────────────────────────────
proj(
    dir="02-build-push-on-tag", id="proj-cicd-tagbuild", title="Project: Build & Push on Tag",
    minutes=40, points=250, prereq="[proj-cicd-lint]",
    theory="""# Project: Build & Push an Image on Tag

Restrict a workflow to version tags with `on: push: tags:`, then build and push
a Docker image for the release.
""",
    instructions="""# Project Tasks

Create `/root/repo/.github/workflows/release.yml`:

1. Trigger only on **tag** pushes (`on: push: tags: ['v*']`).
2. A step that runs **`docker build`** and **`docker push`** for the image.

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo/.github/workflows
exit 0
""",
    solution="""mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/release.yml <<'YML'
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push
        run: |
          docker build -t myapp:${{ github.ref_name }} .
          docker push myapp:${{ github.ref_name }}
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.github/workflows/release.yml
fail=0
[ -f "$F" ] && echo "STEP:release.yml exists:PASS" || { echo "STEP:release.yml exists:FAIL:create release.yml"; exit 1; }
grep -q "tags:" "$F" && echo "STEP:triggered on tags:PASS" || { echo "STEP:triggered on tags:FAIL:trigger on tag pushes"; fail=1; }
grep -q "docker build" "$F" && grep -q "docker push" "$F" && echo "STEP:builds and pushes image:PASS" || { echo "STEP:builds and pushes image:FAIL:docker build + push"; fail=1; }
exit $fail
""",
)

# ── 03 multi-stage pipeline ──────────────────────────────
proj(
    dir="03-multistage-pipeline", id="proj-cicd-pipeline", title="Project: Build → Test → Deploy",
    minutes=40, points=300, prereq="[proj-cicd-tagbuild]",
    theory="""# Project: Multi-stage Pipeline

Real pipelines have ordered jobs. In Actions, `needs:` makes one job wait for
another — `build` → `test` → `deploy`.
""",
    instructions="""# Project Tasks

Create `/root/repo/.github/workflows/pipeline.yml` with **three jobs** —
`build`, `test`, `deploy` — chained so that `test` **needs** `build` and
`deploy` **needs** `test`.

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo/.github/workflows
exit 0
""",
    solution="""mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/pipeline.yml <<'YML'
name: Pipeline
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo build
  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo test
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo deploy
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.github/workflows/pipeline.yml
fail=0
[ -f "$F" ] && echo "STEP:pipeline.yml exists:PASS" || { echo "STEP:pipeline.yml exists:FAIL:create pipeline.yml"; exit 1; }
if grep -qE "^  build:" "$F" && grep -qE "^  test:" "$F" && grep -qE "^  deploy:" "$F"; then echo "STEP:build/test/deploy jobs:PASS"; else echo "STEP:build/test/deploy jobs:FAIL:define build, test, deploy jobs"; fail=1; fi
n=$(grep -c "needs:" "$F")
[ "${n:-0}" -ge 2 ] && echo "STEP:jobs chained with needs:PASS" || { echo "STEP:jobs chained with needs:FAIL:use needs: to order jobs"; fail=1; }
exit $fail
""",
)

# ── 04 Jenkins ───────────────────────────────────────────
proj(
    dir="04-jenkins-pipeline", id="proj-cicd-jenkins", title="Project: Jenkinsfile Pipeline",
    minutes=40, points=250, prereq="[proj-cicd-pipeline]",
    theory="""# Project: Declarative Jenkinsfile

Jenkins declarative pipelines live in a `Jenkinsfile`: a `pipeline { agent ...
stages { stage('X') { steps { ... } } } }` block.
""",
    instructions="""# Project Tasks

Create `/root/repo/Jenkinsfile` — a **declarative** pipeline with an `agent` and
**`Build`, `Test`, `Deploy`** stages (each with a `steps` block).

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo
exit 0
""",
    solution="""mkdir -p /root/repo
cat > /root/repo/Jenkinsfile <<'JF'
pipeline {
  agent any
  stages {
    stage('Build')  { steps { sh 'make build' } }
    stage('Test')   { steps { sh 'make test' } }
    stage('Deploy') { steps { sh 'make deploy' } }
  }
}
JF
""",
    validate="""#!/bin/sh
F=/root/repo/Jenkinsfile
fail=0
[ -f "$F" ] && echo "STEP:Jenkinsfile exists:PASS" || { echo "STEP:Jenkinsfile exists:FAIL:create Jenkinsfile"; exit 1; }
grep -q "pipeline" "$F" && grep -q "stages" "$F" && echo "STEP:declarative pipeline with stages:PASS" || { echo "STEP:declarative pipeline with stages:FAIL:use pipeline { stages { } }"; fail=1; }
if grep -q "stage('Build')" "$F" && grep -q "stage('Test')" "$F" && grep -q "stage('Deploy')" "$F"; then echo "STEP:Build/Test/Deploy stages:PASS"; else echo "STEP:Build/Test/Deploy stages:FAIL:add Build, Test, Deploy stages"; fail=1; fi
exit $fail
""",
)

# ── 05 GitLab CI ─────────────────────────────────────────
proj(
    dir="05-gitlab-ci", id="proj-cicd-gitlab", title="Project: GitLab CI (cache + artifacts)",
    minutes=40, points=250, prereq="[proj-cicd-jenkins]",
    theory="""# Project: GitLab CI

`.gitlab-ci.yml` defines `stages:` and jobs. `cache:` speeds up repeated runs;
`artifacts:` pass build outputs between stages.
""",
    instructions="""# Project Tasks

Create `/root/repo/.gitlab-ci.yml` that:

1. Declares **`stages:`** (e.g. build, test).
2. Has a build job using **`cache:`**.
3. Produces **`artifacts:`**.

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo
exit 0
""",
    solution="""mkdir -p /root/repo
cat > /root/repo/.gitlab-ci.yml <<'YML'
stages:
  - build
  - test
build:
  stage: build
  cache:
    paths:
      - .cache/
  script:
    - make build
  artifacts:
    paths:
      - dist/
test:
  stage: test
  script:
    - make test
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.gitlab-ci.yml
fail=0
[ -f "$F" ] && echo "STEP:.gitlab-ci.yml exists:PASS" || { echo "STEP:.gitlab-ci.yml exists:FAIL:create .gitlab-ci.yml"; exit 1; }
grep -q "stages:" "$F" && echo "STEP:defines stages:PASS" || { echo "STEP:defines stages:FAIL:add stages:"; fail=1; }
grep -q "cache:" "$F" && echo "STEP:uses cache:PASS" || { echo "STEP:uses cache:FAIL:add a cache:"; fail=1; }
grep -q "artifacts:" "$F" && echo "STEP:produces artifacts:PASS" || { echo "STEP:produces artifacts:FAIL:add artifacts:"; fail=1; }
exit $fail
""",
)

# ── 06 deploy on merge ───────────────────────────────────
proj(
    dir="06-deploy-on-merge", id="proj-cicd-deploy", title="Project: Auto-deploy on Merge",
    minutes=35, points=250, prereq="[proj-cicd-gitlab]",
    theory="""# Project: Deploy on Merge to main

Gate deploys to the default branch: `on: push: branches: [main]`, then publish
the built site to the web server's document root.
""",
    instructions="""# Project Tasks

Create `/root/repo/.github/workflows/deploy.yml`:

1. Triggered on **push to `main`**.
2. A step that publishes the site to the **Nginx web root**
   (`/usr/share/nginx/html/`).

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo/.github/workflows
exit 0
""",
    solution="""mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/deploy.yml <<'YML'
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish to nginx
        run: cp -r site/* /usr/share/nginx/html/
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.github/workflows/deploy.yml
fail=0
[ -f "$F" ] && echo "STEP:deploy.yml exists:PASS" || { echo "STEP:deploy.yml exists:FAIL:create deploy.yml"; exit 1; }
grep -q "branches:" "$F" && grep -q "main" "$F" && echo "STEP:triggers on push to main:PASS" || { echo "STEP:triggers on push to main:FAIL:limit to branch main"; fail=1; }
grep -q "nginx/html" "$F" && echo "STEP:deploys to nginx web root:PASS" || { echo "STEP:deploys to nginx web root:FAIL:publish to /usr/share/nginx/html/"; fail=1; }
exit $fail
""",
)

# ── 07 matrix ────────────────────────────────────────────
proj(
    dir="07-matrix-builds", id="proj-cicd-matrix", title="Project: Matrix Builds",
    minutes=35, points=250, prereq="[proj-cicd-deploy]",
    theory="""# Project: Matrix Builds

A build **matrix** runs the same job across multiple versions in parallel via
`strategy: matrix:`.
""",
    instructions="""# Project Tasks

Create `/root/repo/.github/workflows/matrix.yml` that uses a
**`strategy: matrix`** to test across at least **three** versions
(e.g. Python `3.10`, `3.11`, `3.12`).

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo/.github/workflows
exit 0
""",
    solution="""mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/matrix.yml <<'YML'
name: Matrix
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        version: ["3.10", "3.11", "3.12"]
    steps:
      - run: echo "testing ${{ matrix.version }}"
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.github/workflows/matrix.yml
fail=0
[ -f "$F" ] && echo "STEP:matrix.yml exists:PASS" || { echo "STEP:matrix.yml exists:FAIL:create matrix.yml"; exit 1; }
grep -q "strategy:" "$F" && grep -q "matrix:" "$F" && echo "STEP:uses a build matrix:PASS" || { echo "STEP:uses a build matrix:FAIL:add strategy: matrix:"; fail=1; }
if grep -q "3.10" "$F" && grep -q "3.12" "$F"; then echo "STEP:tests multiple versions:PASS"; else echo "STEP:tests multiple versions:FAIL:include >=3 versions"; fail=1; fi
exit $fail
""",
)

# ── 08 notifications ─────────────────────────────────────
proj(
    dir="08-notifications", id="proj-cicd-notify", title="Project: Pipeline Notifications",
    minutes=35, points=250, prereq="[proj-cicd-matrix]",
    theory="""# Project: Notify on Status

Post pipeline results to Slack/Discord via a webhook stored as a **secret** —
never inline the URL.
""",
    instructions="""# Project Tasks

Create `/root/repo/.github/workflows/notify.yml` with a step that posts a
**Slack or Discord** notification using a **webhook from `secrets`**
(e.g. `${{ secrets.SLACK_WEBHOOK }}`). Use `if: always()` so it fires on
success or failure.

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo/.github/workflows
exit 0
""",
    solution="""mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/notify.yml <<'YML'
name: Notify
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo build
      - name: Notify Slack
        if: always()
        run: curl -X POST -d 'text=build done' ${{ secrets.SLACK_WEBHOOK }}
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.github/workflows/notify.yml
fail=0
[ -f "$F" ] && echo "STEP:notify.yml exists:PASS" || { echo "STEP:notify.yml exists:FAIL:create notify.yml"; exit 1; }
grep -qiE "slack|discord|webhook" "$F" && echo "STEP:has a notification step:PASS" || { echo "STEP:has a notification step:FAIL:post to Slack/Discord"; fail=1; }
grep -q "secrets\\." "$F" && echo "STEP:webhook comes from a secret:PASS" || { echo "STEP:webhook comes from a secret:FAIL:use \\${{ secrets.* }}"; fail=1; }
exit $fail
""",
)

# ── 09 secrets ───────────────────────────────────────────
proj(
    dir="09-pipeline-secrets", id="proj-cicd-secrets", title="Project: Secrets in Pipelines",
    minutes=35, points=300, prereq="[proj-cicd-notify]",
    theory="""# Project: Secrets, Done Right

Inject credentials from the secret store at runtime; pipe them via stdin
(`--password-stdin`). Never commit a password or token.
""",
    instructions="""# Project Tasks

Create `/root/repo/.github/workflows/secure.yml` that logs in to a registry
using a **token from `secrets`** (e.g. `${{ secrets.REGISTRY_TOKEN }}`) via
`--password-stdin`. It must contain **no hardcoded credentials**.

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo/.github/workflows
exit 0
""",
    solution="""mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/secure.yml <<'YML'
name: Secure
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Registry login
        run: echo "${{ secrets.REGISTRY_TOKEN }}" | docker login -u ci --password-stdin
YML
""",
    validate="""#!/bin/sh
F=/root/repo/.github/workflows/secure.yml
fail=0
[ -f "$F" ] && echo "STEP:secure.yml exists:PASS" || { echo "STEP:secure.yml exists:FAIL:create secure.yml"; exit 1; }
grep -q "secrets\\." "$F" && echo "STEP:uses secrets context:PASS" || { echo "STEP:uses secrets context:FAIL:reference \\${{ secrets.* }}"; fail=1; }
if grep -qiE "password[=:][[:space:]]*[A-Za-z0-9]{4,}" "$F"; then echo "STEP:no hardcoded credentials:FAIL:remove the literal password"; fail=1; else echo "STEP:no hardcoded credentials:PASS"; fi
exit $fail
""",
)

# ── 10 blue-green (runnable) ─────────────────────────────
proj(
    dir="10-blue-green", id="proj-cicd-bluegreen", title="Project: Blue-Green Deploy",
    minutes=45, points=350, prereq="[proj-cicd-secrets]",
    theory="""# Project: Blue-Green Deployment

Run two environments — **blue** and **green** — and flip a pointer between them
for zero-downtime releases. Here `current` is a symlink the script switches.
""",
    instructions="""# Project Tasks

`setup.sh` made `/root/deploy/` with `blue/` and `green/` releases and a
`current` symlink pointing at `blue`. Write `/root/deploy/bluegreen.sh` that:

1. Reads which color `current` points at.
2. **Switches** `current` to the *other* color (blue↔green), atomically
   (`ln -sfn`).
3. Appends a line to `/root/deploy/switch.log`.

Running it once should flip `blue → green`; running again flips back. Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf deploy
mkdir -p deploy/blue deploy/green
echo v-blue > deploy/blue/index.html
echo v-green > deploy/green/index.html
ln -sfn blue deploy/current
exit 0
""",
    solution="""cat > /root/deploy/bluegreen.sh <<'SH'
#!/bin/bash
set -euo pipefail
cd /root/deploy
current=$(readlink current)
if [ "$current" = "blue" ]; then next=green; else next=blue; fi
ln -sfn "$next" current
echo "$(date '+%F %T') switched $current -> $next" >> switch.log
SH
chmod +x /root/deploy/bluegreen.sh
""",
    validate="""#!/bin/sh
cd /root/deploy 2>/dev/null || { echo "STEP:deploy dir exists:FAIL:/root/deploy missing"; exit 1; }
fail=0
[ -x bluegreen.sh ] && echo "STEP:bluegreen.sh is executable:PASS" || { echo "STEP:bluegreen.sh is executable:FAIL:create executable bluegreen.sh"; exit 1; }
ln -sfn blue current
./bluegreen.sh >/dev/null 2>&1
if [ "$(readlink current)" = "green" ]; then echo "STEP:switches blue -> green:PASS"; else echo "STEP:switches blue -> green:FAIL:current should point at green"; fail=1; fi
./bluegreen.sh >/dev/null 2>&1
if [ "$(readlink current)" = "blue" ]; then echo "STEP:toggles green -> blue:PASS"; else echo "STEP:toggles green -> blue:FAIL:second run should switch back to blue"; fail=1; fi
[ -s switch.log ] && echo "STEP:logs each switch:PASS" || { echo "STEP:logs each switch:FAIL:append to switch.log"; fail=1; }
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
            f"track: cicd\nlevel: intermediate\n"
            f"estimated_minutes: {p['minutes']}\n"
            f"image: lab-linux:latest\n"
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
    print(f"Wrote {len(PROJECTS)} CI/CD projects to {BASE}")


if __name__ == "__main__":
    main()
