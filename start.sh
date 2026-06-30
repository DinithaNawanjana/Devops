#!/usr/bin/env bash
# One-command start for the DevOps Learning Platform.
#
#   git clone <repo> && cd Devops && ./start.sh
#
# Requires: Docker + Docker Compose. Brings up web + api + db + redis.
set -euo pipefail
cd "$(dirname "$0")"

# 0. Preflight: the Docker daemon must be reachable. On Windows/macOS this
#    means Docker Desktop has to be running ("Engine running").
if ! docker info >/dev/null 2>&1; then
  cat >&2 <<'ERR'
✗ Cannot reach the Docker engine.

  Docker Desktop is probably not running. Start it and wait until it shows
  "Engine running", then re-run ./start.sh. Verify with:  docker info

  (On Windows, run this script from Git Bash or WSL, with Docker Desktop's
   WSL 2 backend enabled.)
ERR
  exit 1
fi

# 1. Create .env on first run.
if [ ! -f .env ]; then
  cp .env.example .env
  echo "✓ created .env from .env.example (edit JWT_SECRET for anything real)"
fi

# 2. Build the lab sandbox images (skip with SKIP_LAB_IMAGES=1).
if [ "${SKIP_LAB_IMAGES:-0}" != "1" ]; then
  echo "▶ Building lab sandbox images (first run can take a few minutes)…"
  ./scripts/build-lab-images.sh || echo "⚠ lab image build failed — the web app still runs; labs need these images."
fi

# 3. Launch the platform.
echo "▶ Starting the platform…"
docker compose up --build -d

cat <<'EOF'

✅ Up. Open:
   • Web app : http://localhost:3000
   • API docs: http://localhost:8000/docs

Logs : docker compose logs -f
Stop : docker compose down
EOF
