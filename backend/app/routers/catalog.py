"""Read-only catalog: tracks + labs loaded from disk content."""
from fastapi import APIRouter, HTTPException

from .. import content_loader
from ..schemas import LabDetail, LabSummary, TrackOut

router = APIRouter(tags=["catalog"])


@router.get("/tracks", response_model=list[TrackOut])
async def tracks():
    return content_loader.list_tracks()


@router.get("/labs", response_model=list[LabSummary])
async def labs(track: str | None = None):
    return content_loader.list_labs(track)


@router.get("/labs/{lab_id}", response_model=LabDetail)
async def lab_detail(lab_id: str):
    lab = content_loader.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab.detail()


@router.post("/content/reload")
async def reload_content():
    """Re-scan the content dir (handy after authoring new labs)."""
    content_loader.reload()
    return {"status": "reloaded", "tracks": len(content_loader.list_tracks())}
