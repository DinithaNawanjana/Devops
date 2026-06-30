# Solution

```bash
mkdir -p /root/sec/.github/workflows
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
```
