# Project Tasks

Create `/root/repo/.github/workflows/release.yml`:

1. Trigger only on **tag** pushes (`on: push: tags: ['v*']`).
2. A step that runs **`docker build`** and **`docker push`** for the image.

Click **Check**.
