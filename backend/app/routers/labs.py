"""Lab sessions: start/stop, the xterm.js WebSocket bridge, and validation."""
from __future__ import annotations

import asyncio
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .. import content_loader
from ..auth import decode_token, get_current_user
from ..config import settings
from ..database import get_db
from ..lab_engine import session_manager
from ..lab_engine.validation import parse
from ..models import LabSession, User
from ..schemas import (
    CheckResult,
    FileContent,
    FileEntry,
    SessionOut,
    WriteFileRequest,
)
from .progress import record_completion

router = APIRouter(prefix="/labs", tags=["labs"])


@router.post("/{lab_id}/start", response_model=SessionOut)
async def start_session(
    lab_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lab = content_loader.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not session_manager.ping():
        raise HTTPException(status_code=503, detail="Docker engine unavailable")

    session_id = str(uuid.uuid4())
    try:
        sess = await asyncio.to_thread(
            session_manager.start, session_id, user.id, lab
        )
    except Exception as exc:  # image missing, daemon error, etc.
        raise HTTPException(status_code=500, detail=f"Could not start lab: {exc}")

    row = LabSession(
        id=session_id,
        user_id=user.id,
        lab_id=lab_id,
        container_id=sess.container_id,
        status="running",
    )
    db.add(row)
    await db.commit()

    return SessionOut(
        id=session_id,
        lab_id=lab_id,
        status="running",
        started_at=row.started_at,
        ws_url=f"{settings_ws_base()}/labs/sessions/{session_id}/terminal",
    )


@router.post("/sessions/{session_id}/stop")
async def stop_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    sess = session_manager.get(session_id)
    if sess and sess.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your session")
    await asyncio.to_thread(session_manager.stop, session_id)

    row = await db.get(LabSession, session_id)
    if row:
        row.status = "stopped"
        await db.commit()
    return {"status": "stopped"}


@router.post("/sessions/{session_id}/check", response_model=CheckResult)
async def check_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    sess = session_manager.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    if sess.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your session")

    lab = content_loader.get_lab(sess.lab_id)
    points = lab.points if lab else 100
    try:
        exit_code, output = await asyncio.to_thread(
            session_manager.run_validation, session_id
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Validation failed to run: {exc}")

    result = parse(exit_code, output, points)
    if result.passed:
        item_type = lab.type if lab else "lab"
        await record_completion(db, user, item_type, sess.lab_id, result.score)
    return result


# ── Editor file access (Monaco) ─────────────────────────────
def _owned_session(session_id: str, user: User):
    sess = session_manager.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    if sess.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your session")
    return sess


@router.get("/sessions/{session_id}/files", response_model=list[FileEntry])
async def list_files(
    session_id: str,
    path: str = "/root",
    user: User = Depends(get_current_user),
):
    _owned_session(session_id, user)
    try:
        return await asyncio.to_thread(session_manager.list_files, session_id, path)
    except PermissionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/sessions/{session_id}/file", response_model=FileContent)
async def read_file(
    session_id: str,
    path: str,
    user: User = Depends(get_current_user),
):
    _owned_session(session_id, user)
    try:
        content = await asyncio.to_thread(session_manager.read_file, session_id, path)
    except PermissionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    return FileContent(path=path, content=content)


@router.put("/sessions/{session_id}/file")
async def write_file(
    session_id: str,
    body: WriteFileRequest,
    user: User = Depends(get_current_user),
):
    _owned_session(session_id, user)
    if len(body.content) > 1_000_000:
        raise HTTPException(status_code=413, detail="File too large (max 1MB)")
    try:
        await asyncio.to_thread(
            session_manager.write_file, session_id, body.path, body.content
        )
    except PermissionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except OSError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"status": "saved", "path": body.path}


# ── WebSocket terminal bridge (xterm.js ↔ container shell) ──
@router.websocket("/sessions/{session_id}/terminal")
async def terminal(websocket: WebSocket, session_id: str, token: str | None = None):
    """Bidirectional bridge: browser keystrokes → container stdin,
    container stdout → browser. Auth via ?token=<jwt> query param.
    """
    await websocket.accept()

    # Authenticate the socket (browsers can't set Authorization on WS).
    try:
        user_id = decode_token(token or "")
    except HTTPException:
        await websocket.close(code=4401)
        return

    sess = session_manager.get(session_id)
    if not sess or sess.user_id != user_id:
        await websocket.close(code=4404)
        return

    # Open an interactive exec with a PTY against the running container.
    client = session_manager.client
    try:
        exec_id = client.api.exec_create(
            sess.container_id,
            cmd="/bin/bash",
            tty=True,
            stdin=True,
            workdir="/root",
        )["Id"]
        sock = client.api.exec_start(exec_id, tty=True, stream=False, socket=True)
    except Exception as exc:
        await websocket.send_text(f"\r\n[lab] failed to attach: {exc}\r\n")
        await websocket.close(code=1011)
        return

    raw = sock._sock  # underlying socket
    raw.setblocking(False)
    loop = asyncio.get_event_loop()

    async def pump_container_to_ws():
        while True:
            try:
                data = await loop.sock_recv(raw, 4096)
            except (BlockingIOError, InterruptedError):
                await asyncio.sleep(0.02)
                continue
            except OSError:
                break
            if not data:
                break
            sess.touch()
            await websocket.send_bytes(data)

    async def pump_ws_to_container():
        while True:
            msg = await websocket.receive()
            if msg.get("type") == "websocket.disconnect":
                break
            payload = msg.get("bytes")
            if payload is None and msg.get("text") is not None:
                payload = msg["text"].encode("utf-8")
            if payload:
                sess.touch()
                await loop.sock_sendall(raw, payload)

    out_task = asyncio.create_task(pump_container_to_ws())
    in_task = asyncio.create_task(pump_ws_to_container())
    try:
        await asyncio.wait(
            {out_task, in_task}, return_when=asyncio.FIRST_COMPLETED
        )
    except WebSocketDisconnect:
        pass
    finally:
        for t in (out_task, in_task):
            t.cancel()
        try:
            raw.close()
        except OSError:
            pass


def settings_ws_base() -> str:
    # The browser-facing WS base is configured on the frontend; the relative
    # path is what matters here. Returned for convenience in SessionOut.
    return ""
