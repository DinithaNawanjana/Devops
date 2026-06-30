# Solution

```bash
mkdir -p /root/repo/.github/workflows
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
```
