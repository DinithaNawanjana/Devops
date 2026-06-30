#!/usr/bin/env python3
"""Authoring helper: DevSecOps project set (spec §5). Scanning/signing/policy
config authoring graded structurally.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "devsecops"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


CLEAN = "#!/bin/sh\ncd /root || exit 0\nrm -rf sec\nmkdir -p sec\nexit 0\n"

proj(
    dir="01-trivy-scan", id="proj-sec-trivy", title="Project: Trivy Image Scan in CI",
    minutes=35, points=250, prereq="[docker-01]",
    theory="""# Project: Image Vulnerability Scanning

`trivy` scans container images for known CVEs. Run it in CI and fail the build
on high-severity findings.
""",
    instructions="""# Project Tasks

Create `/root/sec/.github/workflows/scan.yml` — a workflow that runs **`trivy`**
to scan a built image (fail on HIGH/CRITICAL).

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf sec\nmkdir -p sec/.github/workflows\nexit 0\n",
    solution="""mkdir -p /root/sec/.github/workflows
cat > /root/sec/.github/workflows/scan.yml <<'YML'
name: Image Scan
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:latest
          severity: HIGH,CRITICAL
          exit-code: '1'
YML
""",
    validate="""#!/bin/sh
F=/root/sec/.github/workflows/scan.yml
fail=0
[ -f "$F" ] && echo "STEP:scan.yml exists:PASS" || { echo "STEP:scan.yml exists:FAIL:create scan.yml"; exit 1; }
grep -qi "trivy" "$F" && echo "STEP:runs trivy:PASS" || { echo "STEP:runs trivy:FAIL:add a trivy scan step"; fail=1; }
grep -qiE "HIGH|CRITICAL|exit-code" "$F" && echo "STEP:fails on high severity:PASS" || { echo "STEP:fails on high severity:FAIL:gate on HIGH/CRITICAL"; fail=1; }
exit $fail
""",
)

proj(
    dir="02-sast-semgrep", id="proj-sec-sast", title="Project: SAST with Semgrep",
    minutes=35, points=250, prereq="[proj-sec-trivy]",
    theory="""# Project: Static Analysis (SAST)

SAST tools like **Semgrep**/**Bandit** scan source for insecure patterns before
runtime.
""",
    instructions="""# Project Tasks

Create `/root/sec/.github/workflows/sast.yml` that runs **semgrep** (or
**bandit**) over the codebase.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf sec\nmkdir -p sec/.github/workflows\nexit 0\n",
    solution="""mkdir -p /root/sec/.github/workflows
cat > /root/sec/.github/workflows/sast.yml <<'YML'
name: SAST
on: [push]
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep
        run: |
          pip install semgrep
          semgrep --config auto --error
YML
""",
    validate="""#!/bin/sh
F=/root/sec/.github/workflows/sast.yml
fail=0
[ -f "$F" ] && echo "STEP:sast.yml exists:PASS" || { echo "STEP:sast.yml exists:FAIL:create sast.yml"; exit 1; }
grep -qiE "semgrep|bandit" "$F" && echo "STEP:runs a SAST tool:PASS" || { echo "STEP:runs a SAST tool:FAIL:run semgrep or bandit"; fail=1; }
exit $fail
""",
)

proj(
    dir="03-gitleaks", id="proj-sec-gitleaks", title="Project: Secrets Scanning",
    minutes=30, points=250, prereq="[proj-sec-sast]",
    theory="""# Project: Secrets Scanning

`gitleaks` detects committed secrets (keys, tokens). Run it in CI to block leaks.
""",
    instructions="""# Project Tasks

Create `/root/sec/.github/workflows/secrets.yml` that runs **gitleaks** on the
repo.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf sec\nmkdir -p sec/.github/workflows\nexit 0\n",
    solution="""mkdir -p /root/sec/.github/workflows
cat > /root/sec/.github/workflows/secrets.yml <<'YML'
name: Secret Scan
on: [push]
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
YML
""",
    validate="""#!/bin/sh
F=/root/sec/.github/workflows/secrets.yml
fail=0
[ -f "$F" ] && echo "STEP:secrets.yml exists:PASS" || { echo "STEP:secrets.yml exists:FAIL:create secrets.yml"; exit 1; }
grep -qi "gitleaks" "$F" && echo "STEP:runs gitleaks:PASS" || { echo "STEP:runs gitleaks:FAIL:add a gitleaks step"; fail=1; }
exit $fail
""",
)

proj(
    dir="04-vault-secrets", id="proj-sec-vault", title="Project: Vault Secrets",
    minutes=40, points=300, prereq="[proj-sec-gitleaks]",
    theory="""# Project: HashiCorp Vault

Vault stores secrets centrally. `vault kv put` writes, `vault kv get` reads —
apps fetch at runtime instead of baking secrets in.
""",
    instructions="""# Project Tasks

Create `/root/sec/vault.sh` that **stores** a secret with `vault kv put` and
**retrieves** it with `vault kv get`.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/sec
cat > /root/sec/vault.sh <<'SH'
#!/bin/bash
set -euo pipefail
export VAULT_ADDR="http://127.0.0.1:8200"
# Store
vault kv put secret/myapp db_password=s3cr3t
# Retrieve
vault kv get -field=db_password secret/myapp
SH
chmod +x /root/sec/vault.sh
""",
    validate="""#!/bin/sh
F=/root/sec/vault.sh
fail=0
[ -x "$F" ] && echo "STEP:vault.sh exists:PASS" || { echo "STEP:vault.sh exists:FAIL:create executable vault.sh"; exit 1; }
grep -q "vault kv put" "$F" && echo "STEP:stores a secret:PASS" || { echo "STEP:stores a secret:FAIL:use vault kv put"; fail=1; }
grep -q "vault kv get" "$F" && echo "STEP:retrieves a secret:PASS" || { echo "STEP:retrieves a secret:FAIL:use vault kv get"; fail=1; }
exit $fail
""",
)

proj(
    dir="05-cosign-sign", id="proj-sec-cosign", title="Project: Sign & Verify Images",
    minutes=40, points=300, prereq="[proj-sec-vault]",
    theory="""# Project: Image Signing with Cosign

`cosign sign` cryptographically signs an image; `cosign verify` checks it —
proving provenance before deploy.
""",
    instructions="""# Project Tasks

Create `/root/sec/sign.sh` that **signs** an image with `cosign sign` and
**verifies** it with `cosign verify`.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/sec
cat > /root/sec/sign.sh <<'SH'
#!/bin/bash
set -euo pipefail
IMAGE="localhost:5000/myapp:1.0.0"
cosign sign --key cosign.key "$IMAGE"
cosign verify --key cosign.pub "$IMAGE"
SH
chmod +x /root/sec/sign.sh
""",
    validate="""#!/bin/sh
F=/root/sec/sign.sh
fail=0
[ -x "$F" ] && echo "STEP:sign.sh exists:PASS" || { echo "STEP:sign.sh exists:FAIL:create executable sign.sh"; exit 1; }
grep -q "cosign sign" "$F" && echo "STEP:signs the image:PASS" || { echo "STEP:signs the image:FAIL:use cosign sign"; fail=1; }
grep -q "cosign verify" "$F" && echo "STEP:verifies the signature:PASS" || { echo "STEP:verifies the signature:FAIL:use cosign verify"; fail=1; }
exit $fail
""",
)

proj(
    dir="06-opa-policy", id="proj-sec-opa", title="Project: Policy as Code (OPA)",
    minutes=45, points=350, prereq="[proj-sec-cosign]",
    theory="""# Project: Policy as Code

Open Policy Agent (Rego) encodes rules as code. `conftest` runs them against
configs to **deny** non-compliant resources.
""",
    instructions="""# Project Tasks

Create `/root/sec/policy.rego` — a Rego policy in a `package` with a **`deny`**
rule (e.g. deny containers running as root / using the `latest` tag).

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/sec
cat > /root/sec/policy.rego <<'REGO'
package main

deny[msg] {
  input.kind == "Deployment"
  some i
  image := input.spec.template.spec.containers[i].image
  endswith(image, ":latest")
  msg := sprintf("container image %v uses the latest tag", [image])
}
REGO
""",
    validate="""#!/bin/sh
F=/root/sec/policy.rego
fail=0
[ -f "$F" ] && echo "STEP:policy.rego exists:PASS" || { echo "STEP:policy.rego exists:FAIL:create policy.rego"; exit 1; }
grep -q "package" "$F" && echo "STEP:declares a package:PASS" || { echo "STEP:declares a package:FAIL:add a package declaration"; fail=1; }
grep -qE "deny" "$F" && echo "STEP:has a deny rule:PASS" || { echo "STEP:has a deny rule:FAIL:add a deny rule"; fail=1; }
exit $fail
""",
)

proj(
    dir="07-dependency-scan", id="proj-sec-deps", title="Project: Dependency Scanning",
    minutes=35, points=250, prereq="[proj-sec-opa]",
    theory="""# Project: Dependency Updates

Dependabot watches your manifests and opens PRs for vulnerable/outdated deps.
Configure it in `.github/dependabot.yml`.
""",
    instructions="""# Project Tasks

Create `/root/sec/.github/dependabot.yml` with at least one `package-ecosystem`
update on a schedule.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf sec\nmkdir -p sec/.github\nexit 0\n",
    solution="""mkdir -p /root/sec/.github
cat > /root/sec/.github/dependabot.yml <<'YML'
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
YML
""",
    validate="""#!/bin/sh
F=/root/sec/.github/dependabot.yml
fail=0
[ -f "$F" ] && echo "STEP:dependabot.yml exists:PASS" || { echo "STEP:dependabot.yml exists:FAIL:create .github/dependabot.yml"; exit 1; }
grep -q "package-ecosystem" "$F" && echo "STEP:defines an ecosystem:PASS" || { echo "STEP:defines an ecosystem:FAIL:add a package-ecosystem"; fail=1; }
grep -q "schedule:" "$F" && echo "STEP:on a schedule:PASS" || { echo "STEP:on a schedule:FAIL:add a schedule"; fail=1; }
exit $fail
""",
)

proj(
    dir="08-harden-dockerfile", id="proj-sec-harden", title="Project: Harden a Dockerfile",
    minutes=40, points=300, prereq="[proj-sec-deps]",
    theory="""# Project: Dockerfile Hardening

Reduce attack surface: a minimal base, a **non-root** `USER`, no secrets, pinned
versions.
""",
    instructions="""# Project Tasks

Create `/root/sec/Dockerfile` that:

1. Uses a **minimal base** (alpine / slim / distroless).
2. Creates and switches to a **non-root `USER`**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/sec
cat > /root/sec/Dockerfile <<'DF'
FROM python:3.11-alpine
RUN adduser -D appuser
WORKDIR /app
COPY . .
USER appuser
CMD ["python", "app.py"]
DF
""",
    validate="""#!/bin/sh
F=/root/sec/Dockerfile
fail=0
[ -f "$F" ] && echo "STEP:Dockerfile exists:PASS" || { echo "STEP:Dockerfile exists:FAIL:create sec/Dockerfile"; exit 1; }
grep -qiE "alpine|slim|distroless" "$F" && echo "STEP:minimal base image:PASS" || { echo "STEP:minimal base image:FAIL:use alpine/slim/distroless"; fail=1; }
if grep -qE "^USER " "$F" && ! grep -qiE "^USER +root" "$F"; then echo "STEP:runs as non-root:PASS"; else echo "STEP:runs as non-root:FAIL:add a non-root USER"; fail=1; fi
exit $fail
""",
)

proj(
    dir="09-network-policy", id="proj-sec-netpol", title="Project: K8s Network Policy",
    minutes=40, points=300, prereq="[proj-sec-harden]",
    theory="""# Project: Network Policies

By default pods talk freely. A `NetworkPolicy` restricts ingress/egress — default
deny, then allow only what's needed.
""",
    instructions="""# Project Tasks

Create `/root/sec/networkpolicy.yaml` — a `NetworkPolicy` with a `podSelector`
and `policyTypes` that restricts traffic (e.g. default-deny ingress).

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/sec
cat > /root/sec/networkpolicy.yaml <<'YML'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
    - Ingress
YML
""",
    validate="""#!/bin/sh
F=/root/sec/networkpolicy.yaml
fail=0
grep -q "kind: NetworkPolicy" "$F" 2>/dev/null && echo "STEP:NetworkPolicy manifest:PASS" || { echo "STEP:NetworkPolicy manifest:FAIL:create a NetworkPolicy"; exit 1; }
grep -q "podSelector:" "$F" && echo "STEP:has a podSelector:PASS" || { echo "STEP:has a podSelector:FAIL:add a podSelector"; fail=1; }
grep -q "policyTypes:" "$F" && echo "STEP:declares policyTypes:PASS" || { echo "STEP:declares policyTypes:FAIL:add policyTypes"; fail=1; }
exit $fail
""",
)

proj(
    dir="10-secure-pipeline", id="proj-sec-pipeline", title="Project: Secure CI/CD Pipeline",
    minutes=60, points=450, prereq="[proj-sec-netpol]",
    theory="""# Project: Scan → Sign → Deploy

A gated pipeline: scan the image (trivy), sign it (cosign), and only then
deploy — security as a gate, not an afterthought.
""",
    instructions="""# Project Tasks

Create `/root/sec/.github/workflows/secure.yml` with stages that **scan**
(trivy), **sign** (cosign), and **deploy** — deploy gated behind the scan/sign.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf sec\nmkdir -p sec/.github/workflows\nexit 0\n",
    solution="""mkdir -p /root/sec/.github/workflows
cat > /root/sec/.github/workflows/secure.yml <<'YML'
name: Secure Pipeline
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - run: trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest
  sign:
    needs: scan
    runs-on: ubuntu-latest
    steps:
      - run: cosign sign --key cosign.key myapp:latest
  deploy:
    needs: sign
    runs-on: ubuntu-latest
    steps:
      - run: kubectl apply -f k8s/
YML
""",
    validate="""#!/bin/sh
F=/root/sec/.github/workflows/secure.yml
fail=0
[ -f "$F" ] && echo "STEP:secure.yml exists:PASS" || { echo "STEP:secure.yml exists:FAIL:create secure.yml"; exit 1; }
grep -qi "trivy" "$F" && echo "STEP:scans the image:PASS" || { echo "STEP:scans the image:FAIL:add a trivy scan"; fail=1; }
grep -qi "cosign" "$F" && echo "STEP:signs the image:PASS" || { echo "STEP:signs the image:FAIL:add a cosign sign"; fail=1; }
grep -q "needs:" "$F" && grep -qiE "deploy|kubectl" "$F" && echo "STEP:deploy gated behind scan/sign:PASS" || { echo "STEP:deploy gated behind scan/sign:FAIL:gate deploy with needs:"; fail=1; }
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
            f"id: {p['id']}\ntitle: \"{p['title']}\"\ntrack: devsecops\n"
            f"level: advanced\nestimated_minutes: {p['minutes']}\n"
            f"image: lab-docker:latest\nprerequisites: {p['prereq']}\n"
            f"points: {p['points']}\n",
            encoding="utf-8",
        )
        (d / "theory.md").write_text(p["theory"], encoding="utf-8")
        (d / "instructions.md").write_text(p["instructions"], encoding="utf-8")
        write_exec(d / "setup.sh", p["setup"])
        write_exec(d / "validate.sh", p["validate"])
        (d / "solution.md").write_text(
            "# Solution\n\n```bash\n" + p["solution"].strip() + "\n```\n", encoding="utf-8"
        )
        write_exec(d / ".solution.sh", "#!/bin/bash\nset -e\n" + p["solution"])
    print(f"Wrote {len(PROJECTS)} devsecops projects to {BASE}")


if __name__ == "__main__":
    main()
