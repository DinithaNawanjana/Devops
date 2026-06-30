#!/usr/bin/env python3
"""Authoring helper: Advanced/Expert Capstone set (spec §5), spread across the
expert tracks. Mostly structural grading; FinOps and DR capstones are runnable.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CROOT = ROOT / "content" / "projects"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


# 1 GitOps platform (gitops)
proj(
    track="gitops", dir="01-gitops-platform", id="proj-cap-gitops",
    title="Capstone: GitOps Platform (ArgoCD + Helm + multi-env)",
    minutes=90, points=600, prereq="[proj-k8s-argocd]", image="lab-k8s:latest",
    theory="""# Capstone: GitOps Platform

Run dev and prod from Git: ArgoCD `Application`s pointing at a Helm chart, one
per environment, synced automatically.
""",
    instructions="""# Capstone Tasks

In `/root/gitops/`:

1. A Helm chart (`chart/Chart.yaml`).
2. **Two ArgoCD `Application`s** — `app-dev.yaml` and `app-prod.yaml` — targeting
   different namespaces (dev/prod) and the chart.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf gitops\nmkdir -p gitops/chart\nexit 0\n",
    solution="""mkdir -p /root/gitops/chart
cat > /root/gitops/chart/Chart.yaml <<'YML'
apiVersion: v2
name: app
version: 0.1.0
YML
for env in dev prod; do
cat > /root/gitops/app-$env.yaml <<YML
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-$env
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/example/app.git
    path: chart
    helm:
      valueFiles: [values-$env.yaml]
  destination:
    server: https://kubernetes.default.svc
    namespace: $env
  syncPolicy:
    automated: { prune: true, selfHeal: true }
YML
done
""",
    validate="""#!/bin/sh
fail=0
[ -f /root/gitops/chart/Chart.yaml ] && echo "STEP:Helm chart present:PASS" || { echo "STEP:Helm chart present:FAIL:add chart/Chart.yaml"; fail=1; }
n=$(grep -l "kind: Application" /root/gitops/app-*.yaml 2>/dev/null | wc -l)
[ "${n:-0}" -ge 2 ] && echo "STEP:two ArgoCD Applications:PASS" || { echo "STEP:two ArgoCD Applications:FAIL:add app-dev.yaml and app-prod.yaml"; fail=1; }
if grep -hq "namespace: dev" /root/gitops/app-dev.yaml 2>/dev/null && grep -hq "namespace: prod" /root/gitops/app-prod.yaml 2>/dev/null; then echo "STEP:multi-env (dev + prod):PASS"; else echo "STEP:multi-env (dev + prod):FAIL:target dev and prod namespaces"; fail=1; fi
exit $fail
""",
)

# 2 Service mesh (service-mesh)
proj(
    track="service-mesh", dir="01-istio-traffic", id="proj-cap-mesh",
    title="Capstone: Istio Traffic Split + mTLS",
    minutes=80, points=550, prereq="[proj-k8s-multitier]", image="lab-k8s:latest",
    theory="""# Capstone: Service Mesh

Istio shifts traffic between versions with `VirtualService` weights and
enforces mTLS with `PeerAuthentication`.
""",
    instructions="""# Capstone Tasks

In `/root/mesh/`:

1. `virtualservice.yaml` — a `VirtualService` splitting traffic by **weight**
   across two subsets (e.g. 90/10).
2. `peerauth.yaml` — a `PeerAuthentication` enforcing **STRICT mTLS**.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf mesh\nmkdir -p mesh\nexit 0\n",
    solution="""mkdir -p /root/mesh
cat > /root/mesh/virtualservice.yaml <<'YML'
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts: [reviews]
  http:
    - route:
        - destination: { host: reviews, subset: v1 }
          weight: 90
        - destination: { host: reviews, subset: v2 }
          weight: 10
YML
cat > /root/mesh/peerauth.yaml <<'YML'
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
YML
""",
    validate="""#!/bin/sh
fail=0
V=/root/mesh/virtualservice.yaml
grep -q "kind: VirtualService" "$V" 2>/dev/null && grep -q "weight:" "$V" 2>/dev/null && echo "STEP:weighted traffic split:PASS" || { echo "STEP:weighted traffic split:FAIL:add a VirtualService with weights"; fail=1; }
grep -q "kind: PeerAuthentication" /root/mesh/peerauth.yaml 2>/dev/null && grep -qi "STRICT" /root/mesh/peerauth.yaml 2>/dev/null && echo "STEP:STRICT mTLS:PASS" || { echo "STEP:STRICT mTLS:FAIL:enforce STRICT mTLS"; fail=1; }
exit $fail
""",
)

# 3 Chaos (chaos-engineering)
proj(
    track="chaos-engineering", dir="01-pod-chaos", id="proj-cap-chaos",
    title="Capstone: Pod-kill Chaos Experiment",
    minutes=70, points=500, prereq="[proj-k8s-deploy]", image="lab-k8s:latest",
    theory="""# Capstone: Chaos Engineering

Chaos Mesh injects faults. A `PodChaos` with action `pod-kill` randomly kills
pods so you can measure recovery.
""",
    instructions="""# Capstone Tasks

Create `/root/chaos/podchaos.yaml` — a Chaos Mesh **`PodChaos`** experiment with
action **`pod-kill`** targeting an app by selector.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf chaos\nmkdir -p chaos\nexit 0\n",
    solution="""mkdir -p /root/chaos
cat > /root/chaos/podchaos.yaml <<'YML'
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill
spec:
  action: pod-kill
  mode: one
  selector:
    labelSelectors:
      app: web
  duration: 30s
YML
""",
    validate="""#!/bin/sh
F=/root/chaos/podchaos.yaml
fail=0
grep -q "kind: PodChaos" "$F" 2>/dev/null && echo "STEP:PodChaos experiment:PASS" || { echo "STEP:PodChaos experiment:FAIL:create a PodChaos"; exit 1; }
grep -q "pod-kill" "$F" && echo "STEP:pod-kill action:PASS" || { echo "STEP:pod-kill action:FAIL:use action pod-kill"; fail=1; }
grep -q "selector:" "$F" && echo "STEP:targets a selector:PASS" || { echo "STEP:targets a selector:FAIL:add a selector"; fail=1; }
exit $fail
""",
)

# 4 SRE SLO + runbook (sre)
proj(
    track="sre", dir="01-slo-runbook", id="proj-cap-sre",
    title="Capstone: SLOs, Alerting & Runbook",
    minutes=80, points=550, prereq="[proj-mon-slo]", image="lab-linux:latest",
    theory="""# Capstone: SRE Practice

Define SLOs, alert on burn rate, and write the runbook responders follow during
an incident.
""",
    instructions="""# Capstone Tasks

In `/root/sre/`:

1. `slo.yaml` — an SLO with an `objective` (e.g. 99.9%).
2. `alerts.yaml` — a burn-rate `alert` (`expr` with `rate(`).
3. `runbook.md` — incident steps.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf sre\nmkdir -p sre\nexit 0\n",
    solution="""mkdir -p /root/sre
cat > /root/sre/slo.yaml <<'YML'
service: checkout
objective: 99.9
window: 30d
indicator: success_rate
YML
cat > /root/sre/alerts.yaml <<'YML'
groups:
  - name: slo
    rules:
      - alert: ErrorBudgetBurn
        expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.001
        for: 10m
YML
cat > /root/sre/runbook.md <<'MD'
# Runbook: Checkout error-budget burn

1. Check the Grafana SLO dashboard.
2. Identify the failing dependency from traces.
3. Roll back the latest deploy if correlated.
4. Page the on-call lead if budget < 0.
MD
""",
    validate="""#!/bin/sh
fail=0
grep -qi "objective" /root/sre/slo.yaml 2>/dev/null && echo "STEP:SLO with objective:PASS" || { echo "STEP:SLO with objective:FAIL:define an objective in slo.yaml"; fail=1; }
grep -q "rate(" /root/sre/alerts.yaml 2>/dev/null && grep -q "alert:" /root/sre/alerts.yaml 2>/dev/null && echo "STEP:burn-rate alert:PASS" || { echo "STEP:burn-rate alert:FAIL:add a burn-rate alert"; fail=1; }
[ -s /root/sre/runbook.md ] && echo "STEP:runbook written:PASS" || { echo "STEP:runbook written:FAIL:write runbook.md"; fail=1; }
exit $fail
""",
)

# 5 DR backup/restore (sre) — RUNNABLE
proj(
    track="sre", dir="02-dr-backup-restore", id="proj-cap-dr",
    title="Capstone: Backup & Restore (DR)",
    minutes=70, points=500, prereq="[proj-cap-sre]", image="lab-linux:latest",
    theory="""# Capstone: Disaster Recovery

A DR drill: back up a stateful app's data, simulate loss, and restore it. The
restore must reproduce the exact data.
""",
    instructions="""# Capstone Tasks

`setup.sh` created `/root/dr/data/` with app data. Write:

1. `/root/dr/backup.sh` — archive `data/` into `/root/dr/backup.tar.gz`.
2. `/root/dr/restore.sh` — wipe `data/` and restore it from the archive.

The checker backs up, deletes the data, restores, and verifies it returns.
Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf dr
mkdir -p dr/data
echo alpha > dr/data/file1
echo beta  > dr/data/file2
exit 0
""",
    solution="""mkdir -p /root/dr
cat > /root/dr/backup.sh <<'SH'
#!/bin/bash
set -euo pipefail
tar -czf /root/dr/backup.tar.gz -C /root/dr/data .
SH
cat > /root/dr/restore.sh <<'SH'
#!/bin/bash
set -euo pipefail
rm -rf /root/dr/data
mkdir -p /root/dr/data
tar -xzf /root/dr/backup.tar.gz -C /root/dr/data
SH
chmod +x /root/dr/backup.sh /root/dr/restore.sh
""",
    validate="""#!/bin/sh
cd /root/dr 2>/dev/null || { echo "STEP:dr dir exists:FAIL:/root/dr missing"; exit 1; }
fail=0
[ -x backup.sh ] && [ -x restore.sh ] && echo "STEP:backup.sh + restore.sh executable:PASS" || { echo "STEP:backup.sh + restore.sh executable:FAIL:create both scripts"; exit 1; }
./backup.sh >/dev/null 2>&1
[ -f backup.tar.gz ] && echo "STEP:backup archive created:PASS" || { echo "STEP:backup archive created:FAIL:backup.sh should create backup.tar.gz"; fail=1; }
rm -rf data            # simulate disaster
./restore.sh >/dev/null 2>&1
if [ -f data/file1 ] && grep -q alpha data/file1 2>/dev/null; then echo "STEP:data restored after loss:PASS"; else echo "STEP:data restored after loss:FAIL:restore did not recover the data"; fail=1; fi
exit $fail
""",
)

# 6 Backstage IDP (platform-engineering)
proj(
    track="platform-engineering", dir="01-backstage-idp", id="proj-cap-idp",
    title="Capstone: Backstage IDP Slice",
    minutes=75, points=500, prereq="[proj-k8s-helm]", image="lab-linux:latest",
    theory="""# Capstone: Internal Developer Platform

Backstage models software in a catalog (`Component`) and scaffolds new services
with a `Template` — the heart of a golden-path IDP.
""",
    instructions="""# Capstone Tasks

In `/root/idp/`:

1. `catalog-info.yaml` — a Backstage **`Component`**.
2. `template.yaml` — a Backstage **`Template`** (scaffolder).

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf idp\nmkdir -p idp\nexit 0\n",
    solution="""mkdir -p /root/idp
cat > /root/idp/catalog-info.yaml <<'YML'
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: checkout
  annotations:
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: team-a
YML
cat > /root/idp/template.yaml <<'YML'
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: node-service
spec:
  type: service
  parameters: []
  steps: []
YML
""",
    validate="""#!/bin/sh
fail=0
grep -q "kind: Component" /root/idp/catalog-info.yaml 2>/dev/null && grep -q "backstage.io" /root/idp/catalog-info.yaml 2>/dev/null && echo "STEP:Backstage Component:PASS" || { echo "STEP:Backstage Component:FAIL:add a backstage.io Component"; fail=1; }
grep -q "kind: Template" /root/idp/template.yaml 2>/dev/null && echo "STEP:scaffolder Template:PASS" || { echo "STEP:scaffolder Template:FAIL:add a Backstage Template"; fail=1; }
exit $fail
""",
)

# 7 Multi-cluster failover (kubernetes-advanced)
proj(
    track="kubernetes-advanced", dir="01-multicluster-failover", id="proj-cap-multicluster",
    title="Capstone: Multi-cluster Failover",
    minutes=85, points=600, prereq="[proj-k8s-argocd]", image="lab-k8s:latest",
    theory="""# Capstone: Multi-cluster

Run an app on two kind clusters and fail over between them. Define both clusters
and a script that promotes the standby.
""",
    instructions="""# Capstone Tasks

In `/root/mc/`:

1. Two kind cluster configs (`kind: Cluster`): `cluster-primary.yaml`,
   `cluster-standby.yaml`.
2. `failover.sh` that switches the active `kubectl` context to the standby.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf mc\nmkdir -p mc\nexit 0\n",
    solution="""mkdir -p /root/mc
for c in primary standby; do
cat > /root/mc/cluster-$c.yaml <<YML
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: $c
nodes:
  - role: control-plane
YML
done
cat > /root/mc/failover.sh <<'SH'
#!/bin/bash
set -euo pipefail
# Promote the standby cluster by switching context.
kubectl config use-context kind-standby
SH
chmod +x /root/mc/failover.sh
""",
    validate="""#!/bin/sh
fail=0
n=$(grep -l "kind: Cluster" /root/mc/cluster-*.yaml 2>/dev/null | wc -l)
[ "${n:-0}" -ge 2 ] && echo "STEP:two kind clusters defined:PASS" || { echo "STEP:two kind clusters defined:FAIL:add primary + standby cluster configs"; fail=1; }
[ -x /root/mc/failover.sh ] && grep -q "use-context" /root/mc/failover.sh 2>/dev/null && echo "STEP:failover switches context:PASS" || { echo "STEP:failover switches context:FAIL:failover.sh should switch kubectl context"; fail=1; }
exit $fail
""",
)

# 8 Mega capstone (kubernetes-advanced)
proj(
    track="kubernetes-advanced", dir="02-mega-capstone", id="proj-cap-mega",
    title="Capstone: Full Microservices Platform",
    minutes=180, points=1000, prereq="[proj-cap-multicluster]", image="lab-k8s:latest",
    theory="""# Mega-Capstone

Everything at once: CI/CD + IaC + Kubernetes + monitoring + security, all in one
reproducible repo. This is the portfolio centrepiece.
""",
    instructions="""# Capstone Tasks

Assemble `/root/platform/` with one of each pillar:

1. **CI/CD** — `.github/workflows/ci.yml`.
2. **IaC** — a Terraform file (`infra/main.tf`).
3. **Kubernetes** — a manifest (`k8s/deployment.yaml`).
4. **Monitoring** — `monitoring/prometheus.yml`.
5. **Security** — a scan step / `security/scan.yml` referencing trivy.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf platform\nmkdir -p platform/.github/workflows platform/infra platform/k8s platform/monitoring platform/security\nexit 0\n",
    solution="""mkdir -p /root/platform/.github/workflows /root/platform/infra /root/platform/k8s /root/platform/monitoring /root/platform/security
echo 'name: CI
on: [push]
jobs: { build: { runs-on: ubuntu-latest, steps: [ { run: make build } ] } }' > /root/platform/.github/workflows/ci.yml
echo 'resource "docker_container" "app" { name = "app" image = "nginx:alpine" }' > /root/platform/infra/main.tf
echo 'apiVersion: apps/v1
kind: Deployment
metadata: { name: app }
spec: { replicas: 2, selector: { matchLabels: { app: app } }, template: { metadata: { labels: { app: app } }, spec: { containers: [ { name: app, image: nginx:alpine } ] } } }' > /root/platform/k8s/deployment.yaml
echo 'scrape_configs:
  - job_name: app
    static_configs:
      - targets: [app:8080]' > /root/platform/monitoring/prometheus.yml
echo 'name: Scan
on: [push]
jobs: { scan: { runs-on: ubuntu-latest, steps: [ { run: trivy image myapp:latest } ] } }' > /root/platform/security/scan.yml
""",
    validate="""#!/bin/sh
P=/root/platform
fail=0
[ -f "$P/.github/workflows/ci.yml" ] && echo "STEP:CI/CD pipeline:PASS" || { echo "STEP:CI/CD pipeline:FAIL:add .github/workflows/ci.yml"; fail=1; }
ls "$P"/infra/*.tf >/dev/null 2>&1 && echo "STEP:IaC (Terraform):PASS" || { echo "STEP:IaC (Terraform):FAIL:add infra/*.tf"; fail=1; }
grep -rq "kind: Deployment" "$P/k8s" 2>/dev/null && echo "STEP:Kubernetes manifests:PASS" || { echo "STEP:Kubernetes manifests:FAIL:add a k8s Deployment"; fail=1; }
grep -rq "scrape_configs" "$P/monitoring" 2>/dev/null && echo "STEP:Monitoring config:PASS" || { echo "STEP:Monitoring config:FAIL:add monitoring/prometheus.yml"; fail=1; }
grep -rqi "trivy" "$P/security" 2>/dev/null && echo "STEP:Security scanning:PASS" || { echo "STEP:Security scanning:FAIL:add a trivy scan"; fail=1; }
exit $fail
""",
)

# 9 End-to-end pipeline (advanced-cicd)
proj(
    track="advanced-cicd", dir="01-e2e-pipeline", id="proj-cap-e2e",
    title="Capstone: End-to-end Pipeline",
    minutes=90, points=600, prereq="[proj-cicd-secrets]", image="lab-linux:latest",
    theory="""# Capstone: Code → Build → Scan → Deploy → Observe

One pipeline that takes a commit all the way to production and wires up
observability — every gate chained with `needs`.
""",
    instructions="""# Capstone Tasks

Create `/root/pipeline/.github/workflows/e2e.yml` with chained jobs covering
**build**, **scan** (trivy), **deploy** (kubectl/helm), and **observe**
(a monitoring/smoke check) — each gated with `needs:`.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf pipeline\nmkdir -p pipeline/.github/workflows\nexit 0\n",
    solution="""mkdir -p /root/pipeline/.github/workflows
cat > /root/pipeline/.github/workflows/e2e.yml <<'YML'
name: E2E
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [ { run: docker build -t myapp:${{ github.sha }} . } ]
  scan:
    needs: build
    runs-on: ubuntu-latest
    steps: [ { run: trivy image --exit-code 1 myapp:${{ github.sha }} } ]
  deploy:
    needs: scan
    runs-on: ubuntu-latest
    steps: [ { run: helm upgrade --install myapp ./chart } ]
  observe:
    needs: deploy
    runs-on: ubuntu-latest
    steps: [ { run: curl -fsS http://myapp/healthz } ]
YML
""",
    validate="""#!/bin/sh
F=/root/pipeline/.github/workflows/e2e.yml
fail=0
[ -f "$F" ] && echo "STEP:e2e.yml exists:PASS" || { echo "STEP:e2e.yml exists:FAIL:create e2e.yml"; exit 1; }
grep -qi "trivy" "$F" && echo "STEP:scan stage:PASS" || { echo "STEP:scan stage:FAIL:add a scan stage"; fail=1; }
grep -qiE "helm|kubectl" "$F" && echo "STEP:deploy stage:PASS" || { echo "STEP:deploy stage:FAIL:add a deploy stage"; fail=1; }
c=$(grep -c "needs:" "$F"); [ "${c:-0}" -ge 3 ] && echo "STEP:stages chained build->scan->deploy->observe:PASS" || { echo "STEP:stages chained build->scan->deploy->observe:FAIL:chain 4 stages with needs"; fail=1; }
exit $fail
""",
)

# 10 FinOps cost dashboard (finops) — RUNNABLE
proj(
    track="finops", dir="01-cost-dashboard", id="proj-cap-finops",
    title="Capstone: FinOps Cost Report",
    minutes=70, points=500, prereq="[]", image="lab-linux:latest",
    theory="""# Capstone: FinOps

Turn a raw cloud bill into insight: total spend and the costliest service —
the first step toward optimization and tagging strategy.
""",
    instructions="""# Capstone Tasks

`setup.sh` created `/root/finops/bill.csv` (`service,cost` rows). Write
`/root/finops/cost-report.sh` that writes:

1. `/root/finops/total.txt` — total spend across all rows.
2. `/root/finops/top.txt` — the single costliest **service** (summed).

Click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf finops
mkdir -p finops
cat > finops/bill.csv <<'CSV'
service,cost
compute,120.50
storage,30.00
database,80.00
compute,19.50
CSV
exit 0
""",
    solution="""mkdir -p /root/finops
cat > /root/finops/cost-report.sh <<'SH'
#!/bin/bash
set -euo pipefail
cd /root/finops
# Total (skip header)
awk -F, 'NR>1 {sum+=$2} END {printf "%.2f\\n", sum}' bill.csv > total.txt
# Costliest service (sum per service, pick max)
awk -F, 'NR>1 {s[$1]+=$2} END {for (k in s) printf "%s %.2f\\n", k, s[k]}' bill.csv \
  | sort -k2 -rn | head -1 | awk '{print $1}' > top.txt
SH
chmod +x /root/finops/cost-report.sh
""",
    validate="""#!/bin/sh
cd /root/finops 2>/dev/null || { echo "STEP:finops dir exists:FAIL:/root/finops missing"; exit 1; }
fail=0
[ -x cost-report.sh ] && echo "STEP:cost-report.sh executable:PASS" || { echo "STEP:cost-report.sh executable:FAIL:create cost-report.sh"; exit 1; }
./cost-report.sh >/dev/null 2>&1
t=$(tr -dc '0-9' < total.txt 2>/dev/null)
if [ "$t" = "25000" ]; then echo "STEP:total spend = 250.00:PASS"; else echo "STEP:total spend = 250.00:FAIL:total.txt should be 250.00 (got $(cat total.txt 2>/dev/null))"; fail=1; fi
if grep -qi "compute" top.txt 2>/dev/null; then echo "STEP:costliest service = compute:PASS"; else echo "STEP:costliest service = compute:FAIL:top.txt should be compute"; fail=1; fi
exit $fail
""",
)


def write_exec(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main():
    for p in PROJECTS:
        d = CROOT / p["track"] / p["dir"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "project.yaml").write_text(
            f"id: {p['id']}\ntitle: \"{p['title']}\"\ntrack: {p['track']}\n"
            f"level: expert\nestimated_minutes: {p['minutes']}\n"
            f"image: {p['image']}\nprerequisites: {p['prereq']}\n"
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
    print(f"Wrote {len(PROJECTS)} capstone projects")


if __name__ == "__main__":
    main()
