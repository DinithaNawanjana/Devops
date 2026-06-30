# Solution

```bash
mkdir -p /root/sec/.github/workflows
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
```
