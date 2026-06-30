# Capstone Tasks

Create `/root/pipeline/.github/workflows/e2e.yml` with chained jobs covering
**build**, **scan** (trivy), **deploy** (kubectl/helm), and **observe**
(a monitoring/smoke check) — each gated with `needs:`.

Click **Check**.
