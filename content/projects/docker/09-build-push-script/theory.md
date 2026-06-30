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
