# Project Tasks

In `/root/cicd/` create a `Dockerfile` and a **`build.sh`** that:

1. Reads an **`IMAGE`** and a **`VERSION`** from variables (with defaults) —
   no hardcoded passwords/tokens.
2. Runs **`docker build`** tagging `"$IMAGE:$VERSION"`.
3. Runs **`docker push "$IMAGE:$VERSION"`** (default `IMAGE=localhost:5000/myapp`).

A local registry is started for you by the checker. Click **Check**.
