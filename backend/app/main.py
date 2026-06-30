"""FastAPI entrypoint — wires routers, DB init, and the idle-reaper loop."""
import asyncio
import contextlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .lab_engine import session_manager
from .routers import auth, catalog, labs, progress

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("devops-platform")


async def _reaper_loop():
    """Periodically tear down idle / expired lab containers."""
    while True:
        await asyncio.sleep(60)
        try:
            n = await asyncio.to_thread(session_manager.reap)
            if n:
                log.info("reaped %d idle/expired lab session(s)", n)
        except Exception as exc:  # never let the loop die
            log.warning("reaper error: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Clean up sandboxes orphaned by a previous crash/restart.
    try:
        removed = await asyncio.to_thread(session_manager.cleanup_orphans)
        if removed:
            log.info("cleaned up %d orphaned lab container(s)", removed)
    except Exception as exc:
        log.warning("orphan cleanup skipped: %s", exc)

    task = asyncio.create_task(_reaper_loop())
    try:
        yield
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task


app = FastAPI(title="DevOps Learning Platform API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(labs.router)
app.include_router(progress.router)


@app.get("/health")
async def health():
    return {"status": "ok", "docker": session_manager.ping()}
