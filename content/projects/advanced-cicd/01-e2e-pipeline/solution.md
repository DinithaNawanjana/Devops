# Solution

```bash
mkdir -p /root/pipeline/.github/workflows
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
```
