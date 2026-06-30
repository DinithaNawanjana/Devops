#!/usr/bin/env python3
"""Authoring helper: Kubernetes project set (spec §5). Manifest/Helm/ArgoCD
authoring graded structurally; learners apply them for real (kind) in lab-k8s.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "kubernetes"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


CLEAN = "#!/bin/sh\ncd /root || exit 0\nrm -rf k8s\nmkdir -p k8s\nexit 0\n"

# 01 pod + service
proj(
    dir="01-pod-service", id="proj-k8s-pod", title="Project: Pod + Service",
    minutes=35, points=250, prereq="[docker-01]",
    theory="""# Project: Pod + Service

A **Pod** runs containers; a **Service** gives them a stable virtual IP and DNS
name, load-balancing across matching pods via a label `selector`.
""",
    instructions="""# Project Tasks

In `/root/k8s/`:

1. `pod.yaml` — a `Pod` (e.g. nginx) with labels.
2. `service.yaml` — a `Service` whose `selector` matches the pod's labels.

Apply with `kubectl apply -f .`. Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/pod.yaml <<'YML'
apiVersion: v1
kind: Pod
metadata:
  name: web
  labels:
    app: web
spec:
  containers:
    - name: nginx
      image: nginx:alpine
      ports:
        - containerPort: 80
YML
cat > /root/k8s/service.yaml <<'YML'
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
YML
""",
    validate="""#!/bin/sh
fail=0
grep -q "kind: Pod" /root/k8s/pod.yaml 2>/dev/null && echo "STEP:Pod manifest:PASS" || { echo "STEP:Pod manifest:FAIL:create pod.yaml (kind: Pod)"; fail=1; }
grep -q "kind: Service" /root/k8s/service.yaml 2>/dev/null && echo "STEP:Service manifest:PASS" || { echo "STEP:Service manifest:FAIL:create service.yaml (kind: Service)"; fail=1; }
grep -q "selector:" /root/k8s/service.yaml 2>/dev/null && echo "STEP:Service selects the pod:PASS" || { echo "STEP:Service selects the pod:FAIL:add a selector matching the pod labels"; fail=1; }
exit $fail
""",
)

# 02 deployment + rollout
proj(
    dir="02-deployment-rollout", id="proj-k8s-deploy", title="Project: Deployment & Rolling Update",
    minutes=40, points=300, prereq="[proj-k8s-pod]",
    theory="""# Project: Deployments

A **Deployment** manages a replica set of pods and supports rolling updates with
zero downtime via `strategy: RollingUpdate`.
""",
    instructions="""# Project Tasks

Create `/root/k8s/deployment.yaml` — a `Deployment` with **3 `replicas`** and an
explicit **`RollingUpdate`** strategy.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/deployment.yaml <<'YML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
YML
""",
    validate="""#!/bin/sh
F=/root/k8s/deployment.yaml
fail=0
grep -q "kind: Deployment" "$F" 2>/dev/null && echo "STEP:Deployment manifest:PASS" || { echo "STEP:Deployment manifest:FAIL:create deployment.yaml"; exit 1; }
grep -qE "replicas: *3" "$F" && echo "STEP:3 replicas:PASS" || { echo "STEP:3 replicas:FAIL:set replicas: 3"; fail=1; }
grep -q "RollingUpdate" "$F" && echo "STEP:rolling update strategy:PASS" || { echo "STEP:rolling update strategy:FAIL:add strategy RollingUpdate"; fail=1; }
exit $fail
""",
)

# 03 configmap + secret
proj(
    dir="03-configmap-secret", id="proj-k8s-config", title="Project: ConfigMaps & Secrets",
    minutes=40, points=300, prereq="[proj-k8s-deploy]",
    theory="""# Project: Config & Secrets

`ConfigMap` holds non-sensitive config, `Secret` holds sensitive values. Inject
them into pods via `envFrom` / `valueFrom`.
""",
    instructions="""# Project Tasks

In `/root/k8s/`:

1. `config.yaml` — a `ConfigMap`.
2. `secret.yaml` — a `Secret`.
3. `pod.yaml` — a pod that **injects** them (`envFrom` or `valueFrom`).

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/config.yaml <<'YML'
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: info
YML
cat > /root/k8s/secret.yaml <<'YML'
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  API_KEY: s3cr3t
YML
cat > /root/k8s/pod.yaml <<'YML'
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
    - name: app
      image: nginx:alpine
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secret
YML
""",
    validate="""#!/bin/sh
fail=0
grep -q "kind: ConfigMap" /root/k8s/config.yaml 2>/dev/null && echo "STEP:ConfigMap:PASS" || { echo "STEP:ConfigMap:FAIL:create a ConfigMap"; fail=1; }
grep -q "kind: Secret" /root/k8s/secret.yaml 2>/dev/null && echo "STEP:Secret:PASS" || { echo "STEP:Secret:FAIL:create a Secret"; fail=1; }
grep -qE "envFrom|valueFrom|configMapRef|secretRef" /root/k8s/pod.yaml 2>/dev/null && echo "STEP:injected into a pod:PASS" || { echo "STEP:injected into a pod:FAIL:inject config/secret into the pod"; fail=1; }
exit $fail
""",
)

# 04 ingress
proj(
    dir="04-ingress", id="proj-k8s-ingress", title="Project: Ingress Routing",
    minutes=40, points=300, prereq="[proj-k8s-config]",
    theory="""# Project: Ingress

An **Ingress** routes external HTTP traffic to Services by host/path — one entry
point for many backends.
""",
    instructions="""# Project Tasks

Create `/root/k8s/ingress.yaml` — an `Ingress` routing **two paths** (or hosts)
to **two different Services**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/ingress.yaml <<'YML'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
spec:
  rules:
    - http:
        paths:
          - path: /app
            pathType: Prefix
            backend:
              service:
                name: app-svc
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-svc
                port:
                  number: 80
YML
""",
    validate="""#!/bin/sh
F=/root/k8s/ingress.yaml
fail=0
grep -q "kind: Ingress" "$F" 2>/dev/null && echo "STEP:Ingress manifest:PASS" || { echo "STEP:Ingress manifest:FAIL:create ingress.yaml"; exit 1; }
n=$(grep -c "path:" "$F")
[ "${n:-0}" -ge 2 ] && echo "STEP:routes two paths:PASS" || { echo "STEP:routes two paths:FAIL:add two path rules"; fail=1; }
n2=$(grep -c "name:" "$F")
[ "${n2:-0}" -ge 2 ] && echo "STEP:to two backend services:PASS" || { echo "STEP:to two backend services:FAIL:route to two services"; fail=1; }
exit $fail
""",
)

# 05 pv/pvc
proj(
    dir="05-pv-pvc", id="proj-k8s-storage", title="Project: Persistent Storage",
    minutes=40, points=300, prereq="[proj-k8s-ingress]",
    theory="""# Project: PV / PVC

A **PersistentVolumeClaim** requests storage; a pod mounts it so data survives
pod restarts.
""",
    instructions="""# Project Tasks

In `/root/k8s/`:

1. `pvc.yaml` — a `PersistentVolumeClaim`.
2. `pod.yaml` — a pod that mounts it (`volumeMounts` + `volumes`).

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/pvc.yaml <<'YML'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 1Gi
YML
cat > /root/k8s/pod.yaml <<'YML'
apiVersion: v1
kind: Pod
metadata:
  name: stateful
spec:
  containers:
    - name: app
      image: nginx:alpine
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data
YML
""",
    validate="""#!/bin/sh
fail=0
grep -q "kind: PersistentVolumeClaim" /root/k8s/pvc.yaml 2>/dev/null && echo "STEP:PVC manifest:PASS" || { echo "STEP:PVC manifest:FAIL:create a PersistentVolumeClaim"; fail=1; }
grep -q "volumeMounts:" /root/k8s/pod.yaml 2>/dev/null && grep -q "persistentVolumeClaim:" /root/k8s/pod.yaml 2>/dev/null && echo "STEP:pod mounts the claim:PASS" || { echo "STEP:pod mounts the claim:FAIL:mount the PVC in the pod"; fail=1; }
exit $fail
""",
)

# 06 hpa
proj(
    dir="06-hpa", id="proj-k8s-hpa", title="Project: Horizontal Pod Autoscaler",
    minutes=35, points=300, prereq="[proj-k8s-storage]",
    theory="""# Project: HPA

A **HorizontalPodAutoscaler** scales a Deployment between `minReplicas` and
`maxReplicas` based on a metric (e.g. CPU).
""",
    instructions="""# Project Tasks

Create `/root/k8s/hpa.yaml` — a `HorizontalPodAutoscaler` targeting a Deployment,
with **`minReplicas`**, **`maxReplicas`**, and a CPU metric target.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/hpa.yaml <<'YML'
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
YML
""",
    validate="""#!/bin/sh
F=/root/k8s/hpa.yaml
fail=0
grep -q "kind: HorizontalPodAutoscaler" "$F" 2>/dev/null && echo "STEP:HPA manifest:PASS" || { echo "STEP:HPA manifest:FAIL:create hpa.yaml"; exit 1; }
grep -q "minReplicas:" "$F" && grep -q "maxReplicas:" "$F" && echo "STEP:min/max replicas set:PASS" || { echo "STEP:min/max replicas set:FAIL:set minReplicas and maxReplicas"; fail=1; }
grep -qi "cpu" "$F" && echo "STEP:CPU metric target:PASS" || { echo "STEP:CPU metric target:FAIL:target a CPU metric"; fail=1; }
exit $fail
""",
)

# 07 multi-tier
proj(
    dir="07-multi-tier", id="proj-k8s-multitier", title="Project: Multi-tier App",
    minutes=50, points=350, prereq="[proj-k8s-hpa]",
    theory="""# Project: Multi-tier App

Frontend, backend, and database — each a Deployment with its own Service so
tiers reach each other by name.
""",
    instructions="""# Project Tasks

Create `/root/k8s/app.yaml` (multi-doc) with **three Deployments** —
`frontend`, `backend`, `db` — and a Service for each.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/app.yaml <<'YML'
apiVersion: apps/v1
kind: Deployment
metadata: { name: frontend }
spec:
  replicas: 1
  selector: { matchLabels: { app: frontend } }
  template:
    metadata: { labels: { app: frontend } }
    spec: { containers: [ { name: web, image: nginx:alpine } ] }
---
apiVersion: v1
kind: Service
metadata: { name: frontend }
spec: { selector: { app: frontend }, ports: [ { port: 80 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: backend }
spec:
  replicas: 1
  selector: { matchLabels: { app: backend } }
  template:
    metadata: { labels: { app: backend } }
    spec: { containers: [ { name: api, image: nginx:alpine } ] }
---
apiVersion: v1
kind: Service
metadata: { name: backend }
spec: { selector: { app: backend }, ports: [ { port: 80 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: db }
spec:
  replicas: 1
  selector: { matchLabels: { app: db } }
  template:
    metadata: { labels: { app: db } }
    spec: { containers: [ { name: db, image: redis:7-alpine } ] }
---
apiVersion: v1
kind: Service
metadata: { name: db }
spec: { selector: { app: db }, ports: [ { port: 6379 } ] }
YML
""",
    validate="""#!/bin/sh
F=/root/k8s/app.yaml
fail=0
d=$(grep -c "kind: Deployment" "$F" 2>/dev/null)
[ "${d:-0}" -ge 3 ] && echo "STEP:three Deployments (tiers):PASS" || { echo "STEP:three Deployments (tiers):FAIL:need frontend, backend, db"; fail=1; }
s=$(grep -c "kind: Service" "$F" 2>/dev/null)
[ "${s:-0}" -ge 3 ] && echo "STEP:a Service per tier:PASS" || { echo "STEP:a Service per tier:FAIL:add a Service for each tier"; fail=1; }
exit $fail
""",
)

# 08 helm
proj(
    dir="08-helm-chart", id="proj-k8s-helm", title="Project: Helm Chart",
    minutes=50, points=350, prereq="[proj-k8s-multitier]",
    theory="""# Project: Helm Chart

A Helm chart packages templated manifests: `Chart.yaml`, `values.yaml`, and
`templates/` using `{{ .Values.* }}`.
""",
    instructions="""# Project Tasks

Create a chart at `/root/k8s/mychart/`:

1. `Chart.yaml` (with `apiVersion` + `name`).
2. `values.yaml`.
3. `templates/deployment.yaml` that uses **`{{ .Values.* }}`**.

Click **Check**.
""",
    setup="#!/bin/sh\ncd /root || exit 0\nrm -rf k8s\nmkdir -p k8s/mychart/templates\nexit 0\n",
    solution="""mkdir -p /root/k8s/mychart/templates
cat > /root/k8s/mychart/Chart.yaml <<'YML'
apiVersion: v2
name: mychart
version: 0.1.0
YML
cat > /root/k8s/mychart/values.yaml <<'YML'
replicaCount: 2
image: nginx:alpine
YML
cat > /root/k8s/mychart/templates/deployment.yaml <<'YML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-web
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: web
          image: {{ .Values.image }}
YML
""",
    validate="""#!/bin/sh
C=/root/k8s/mychart
fail=0
grep -q "apiVersion:" "$C/Chart.yaml" 2>/dev/null && grep -q "name:" "$C/Chart.yaml" 2>/dev/null && echo "STEP:Chart.yaml present:PASS" || { echo "STEP:Chart.yaml present:FAIL:create Chart.yaml"; fail=1; }
[ -f "$C/values.yaml" ] && echo "STEP:values.yaml present:PASS" || { echo "STEP:values.yaml present:FAIL:create values.yaml"; fail=1; }
grep -q "{{ .Values" "$C/templates/deployment.yaml" 2>/dev/null && echo "STEP:template uses .Values:PASS" || { echo "STEP:template uses .Values:FAIL:template with {{ .Values.* }}"; fail=1; }
exit $fail
""",
)

# 09 rbac + quota
proj(
    dir="09-rbac-quota", id="proj-k8s-rbac", title="Project: Namespace, RBAC & Quota",
    minutes=45, points=350, prereq="[proj-k8s-helm]",
    theory="""# Project: Isolation

Isolate a team with a `Namespace`, scope permissions with `Role` +
`RoleBinding`, and cap usage with a `ResourceQuota`.
""",
    instructions="""# Project Tasks

Create `/root/k8s/isolation.yaml` (multi-doc) containing a **`Namespace`**, a
**`Role`** + **`RoleBinding`**, and a **`ResourceQuota`**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/isolation.yaml <<'YML'
apiVersion: v1
kind: Namespace
metadata: { name: team-a }
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: dev, namespace: team-a }
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: dev-binding, namespace: team-a }
subjects:
  - kind: User
    name: alice
roleRef:
  kind: Role
  name: dev
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: v1
kind: ResourceQuota
metadata: { name: quota, namespace: team-a }
spec:
  hard:
    pods: "10"
    requests.cpu: "2"
YML
""",
    validate="""#!/bin/sh
F=/root/k8s/isolation.yaml
fail=0
grep -q "kind: Namespace" "$F" 2>/dev/null && echo "STEP:Namespace:PASS" || { echo "STEP:Namespace:FAIL:add a Namespace"; fail=1; }
grep -q "kind: Role" "$F" 2>/dev/null && grep -q "kind: RoleBinding" "$F" 2>/dev/null && echo "STEP:Role + RoleBinding:PASS" || { echo "STEP:Role + RoleBinding:FAIL:add a Role and RoleBinding"; fail=1; }
grep -q "kind: ResourceQuota" "$F" 2>/dev/null && echo "STEP:ResourceQuota:PASS" || { echo "STEP:ResourceQuota:FAIL:add a ResourceQuota"; fail=1; }
exit $fail
""",
)

# 10 argocd gitops
proj(
    dir="10-argocd-gitops", id="proj-k8s-argocd", title="Project: GitOps with ArgoCD",
    minutes=55, points=400, prereq="[proj-k8s-rbac]",
    theory="""# Project: GitOps with ArgoCD

ArgoCD syncs a cluster to a Git repo. An `Application` CR declares the `source`
repo/path and the `destination` cluster/namespace.
""",
    instructions="""# Project Tasks

Create `/root/k8s/application.yaml` — an ArgoCD **`Application`**
(`argoproj.io`) with a **`source`** (repo + path) and a **`destination`**
(server + namespace), plus a sync policy.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/k8s
cat > /root/k8s/application.yaml <<'YML'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/example/myapp.git
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
YML
""",
    validate="""#!/bin/sh
F=/root/k8s/application.yaml
fail=0
grep -q "kind: Application" "$F" 2>/dev/null && grep -q "argoproj.io" "$F" 2>/dev/null && echo "STEP:ArgoCD Application:PASS" || { echo "STEP:ArgoCD Application:FAIL:create an argoproj.io Application"; exit 1; }
grep -q "source:" "$F" && grep -q "repoURL" "$F" && echo "STEP:declares a Git source:PASS" || { echo "STEP:declares a Git source:FAIL:add source.repoURL"; fail=1; }
grep -q "destination:" "$F" && echo "STEP:declares a destination:PASS" || { echo "STEP:declares a destination:FAIL:add a destination"; fail=1; }
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
            f"id: {p['id']}\ntitle: \"{p['title']}\"\ntrack: kubernetes\n"
            f"level: advanced\nestimated_minutes: {p['minutes']}\n"
            f"image: lab-k8s:latest\nprerequisites: {p['prereq']}\n"
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
    print(f"Wrote {len(PROJECTS)} kubernetes projects to {BASE}")


if __name__ == "__main__":
    main()
