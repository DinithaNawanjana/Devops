"""Lab session manager — spawns, tracks, and tears down sandbox containers.

Talks to the host Docker engine through the mounted socket. Each lab session
is one container created from the lab's image, with:
  * hard memory / cpu caps (protect the host)
  * the lab's setup.sh + validate.sh copied in under /lab
  * a TTL and idle timeout for auto-teardown

This module is intentionally synchronous (docker-py is blocking); callers in
async routes wrap calls with `anyio.to_thread.run_sync` / `asyncio.to_thread`.
"""
from __future__ import annotations

import io
import tarfile
import time
from dataclasses import dataclass, field

import docker
from docker.errors import APIError, NotFound

from ..config import settings
from ..content_loader import Lab

LABEL_OWNER = "devops-platform"


@dataclass
class Session:
    id: str
    user_id: int
    lab_id: str
    container_id: str
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)

    def touch(self) -> None:
        self.last_active = time.time()


def _q(s: str) -> str:
    """Single-quote a string for safe embedding in a /bin/sh command."""
    return "'" + s.replace("'", "'\\''") + "'"


def _sanitize(path: str) -> str:
    """Confine editor file access to the sandbox home; block traversal."""
    p = (path or "/root").strip()
    if not p.startswith("/"):
        p = f"/root/{p}"
    # Reject parent traversal outright — labs only ever touch /root, /lab, /tmp.
    if ".." in p.split("/"):
        raise PermissionError("path traversal not allowed")
    allowed = ("/root", "/home", "/tmp", "/lab", "/app", "/srv", "/var/www")
    if not p.startswith(allowed):
        raise PermissionError(f"path {p} outside allowed roots")
    return p


def _tar_bytes(files: dict[str, str]) -> bytes:
    """Pack {path: content} into an uncompressed tar for put_archive."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for name, content in files.items():
            data = content.encode("utf-8")
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            info.mode = 0o755
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


class LabSessionManager:
    def __init__(self) -> None:
        self._client: docker.DockerClient | None = None
        self._sessions: dict[str, Session] = {}

    # ── docker client (lazy so import never fails without a socket) ──
    @property
    def client(self) -> docker.DockerClient:
        if self._client is None:
            self._client = docker.from_env()
        return self._client

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except Exception:
            return False

    # ── lifecycle ───────────────────────────────────────────
    def start(self, session_id: str, user_id: int, lab: Lab) -> Session:
        """Create + start a sandbox container for `lab` and seed lab files."""
        container = self.client.containers.run(
            image=lab.image,
            command="sleep infinity",  # keep alive; we exec into it
            detach=True,
            tty=True,
            stdin_open=True,
            name=f"lab-{session_id[:8]}",
            hostname="lab",
            working_dir="/root",
            mem_limit=settings.lab_memory_limit,
            nano_cpus=int(settings.lab_cpu_limit * 1_000_000_000),
            pids_limit=256,
            network=settings.lab_network,
            labels={LABEL_OWNER: "1", "lab_id": lab.id, "session_id": session_id},
            # security: drop the worst, no new privileges. Labs needing dind
            # override this in their own image/compose; see README §Security.
            cap_drop=["ALL"],
            security_opt=["no-new-privileges"],
        )

        # Seed setup + validation scripts into /lab inside the container.
        scripts = {
            "validate.sh": lab.validate_script() or "exit 0\n",
            "setup.sh": lab.setup_script() or "#!/bin/sh\n",
        }
        container.put_archive("/", _tar_bytes({f"lab/{k}": v for k, v in scripts.items()}))

        # Run setup.sh (best-effort; failures surface in logs, not fatal).
        container.exec_run("sh -lc 'chmod +x /lab/*.sh && /lab/setup.sh'", detach=False)

        sess = Session(id=session_id, user_id=user_id, lab_id=lab.id, container_id=container.id)
        self._sessions[session_id] = sess
        return sess

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def stop(self, session_id: str) -> None:
        sess = self._sessions.pop(session_id, None)
        if not sess:
            return
        try:
            c = self.client.containers.get(sess.container_id)
            c.remove(force=True)
        except (NotFound, APIError):
            pass

    # ── validation ──────────────────────────────────────────
    def run_validation(self, session_id: str) -> tuple[int, str]:
        """Run /lab/validate.sh inside the session container.

        Returns (exit_code, combined_output). The validate.sh contract:
        emit `STEP:<name>:PASS` / `STEP:<name>:FAIL[:msg]` lines per check
        and exit 0 only if every step passed.
        """
        sess = self._sessions.get(session_id)
        if not sess:
            raise KeyError(session_id)
        sess.touch()
        c = self.client.containers.get(sess.container_id)
        res = c.exec_run("sh -lc 'sh /lab/validate.sh'", demux=False)
        output = res.output.decode("utf-8", errors="replace") if res.output else ""
        return res.exit_code, output

    # ── file access (Monaco editor) ─────────────────────────
    def _container(self, session_id: str):
        sess = self._sessions.get(session_id)
        if not sess:
            raise KeyError(session_id)
        sess.touch()
        return self.client.containers.get(sess.container_id)

    def list_files(self, session_id: str, path: str = "/root") -> list[dict]:
        """List entries in `path`. Returns [{name, type, path}] sorted dirs-first."""
        c = self._container(session_id)
        safe = _sanitize(path)
        # -p appends '/' to directories so we can classify without stat calls.
        res = c.exec_run(f"sh -lc 'ls -1Ap {_q(safe)} 2>/dev/null'")
        if res.exit_code != 0:
            return []
        entries = []
        for line in res.output.decode("utf-8", "replace").splitlines():
            if not line:
                continue
            is_dir = line.endswith("/")
            name = line.rstrip("/")
            entries.append(
                {
                    "name": name,
                    "type": "dir" if is_dir else "file",
                    "path": f"{safe.rstrip('/')}/{name}",
                }
            )
        entries.sort(key=lambda e: (e["type"] != "dir", e["name"]))
        return entries

    def read_file(self, session_id: str, path: str) -> str:
        """Return the text content of a file inside the sandbox."""
        c = self._container(session_id)
        safe = _sanitize(path)
        res = c.exec_run(f"sh -lc 'base64 {_q(safe)} 2>/dev/null'")
        if res.exit_code != 0:
            raise FileNotFoundError(path)
        import base64

        return base64.b64decode(res.output).decode("utf-8", "replace")

    def write_file(self, session_id: str, path: str, content: str) -> None:
        """Overwrite a file inside the sandbox with `content`."""
        import base64

        c = self._container(session_id)
        safe = _sanitize(path)
        b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
        # Pipe through base64 -d so arbitrary bytes survive the shell.
        res = c.exec_run(
            f"sh -lc 'printf %s {_q(b64)} | base64 -d > {_q(safe)}'"
        )
        if res.exit_code != 0:
            raise OSError(res.output.decode("utf-8", "replace"))

    # ── reaping idle / expired containers ───────────────────
    def reap(self) -> int:
        """Tear down sessions past idle timeout or max duration. Returns count."""
        now = time.time()
        idle = settings.lab_idle_timeout_min * 60
        max_age = settings.lab_max_duration_min * 60
        doomed = [
            sid
            for sid, s in self._sessions.items()
            if (now - s.last_active) > idle or (now - s.created_at) > max_age
        ]
        for sid in doomed:
            self.stop(sid)
        return len(doomed)

    def cleanup_orphans(self) -> int:
        """Remove any platform-owned containers not tracked in-process.

        Runs on startup so a crashed/restarted API doesn't leak sandboxes.
        """
        removed = 0
        try:
            containers = self.client.containers.list(
                all=True, filters={"label": LABEL_OWNER}
            )
        except Exception:
            return 0
        tracked = {s.container_id for s in self._sessions.values()}
        for c in containers:
            if c.id not in tracked:
                try:
                    c.remove(force=True)
                    removed += 1
                except APIError:
                    pass
        return removed


# module-level singleton
session_manager = LabSessionManager()
