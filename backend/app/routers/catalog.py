"""Read-only catalog: tracks, labs, projects, solutions, and the skill tree."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import content_loader
from ..auth import get_current_user
from ..database import get_db
from ..models import Progress, User
from ..schemas import LabDetail, LabSummary, SkillNode, SolutionOut, TrackOut

router = APIRouter(tags=["catalog"])


@router.get("/tracks", response_model=list[TrackOut])
async def tracks():
    return content_loader.list_tracks()


@router.get("/labs", response_model=list[LabSummary])
async def labs(track: str | None = None):
    return content_loader.list_labs(track, kind="lab")


@router.get("/projects", response_model=list[LabSummary])
async def projects(track: str | None = None):
    return content_loader.list_labs(track, kind="project")


@router.get("/labs/{lab_id}", response_model=LabDetail)
async def lab_detail(lab_id: str):
    lab = content_loader.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab.detail()


@router.get("/labs/{lab_id}/solution", response_model=SolutionOut)
async def lab_solution(lab_id: str, user: User = Depends(get_current_user)):
    """Reveal the solution. Requires auth (learner has attempted the lab)."""
    lab = content_loader.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    html = lab.solution_html()
    if not html:
        raise HTTPException(status_code=404, detail="No solution provided")
    return SolutionOut(solution_html=html)


@router.get("/skilltree", response_model=list[SkillNode])
async def skilltree(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """All labs + projects with per-user lock status.

    A node is `completed` if the user finished it, `available` if every
    prerequisite is completed, else `locked`.
    """
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user.id, Progress.status == "completed"
        )
    )
    done = {p.item_id for p in result.scalars().all()}

    nodes: list[SkillNode] = []
    for item in content_loader.list_all():
        if item.id in done:
            status = "completed"
        elif all(pre in done for pre in item.prerequisites):
            status = "available"
        else:
            status = "locked"
        nodes.append(
            SkillNode(
                id=item.id,
                track=item.track,
                title=item.title,
                level=item.level,
                type=item.type,
                points=item.points,
                prerequisites=item.prerequisites,
                status=status,
            )
        )
    return nodes


@router.post("/content/reload")
async def reload_content():
    """Re-scan the content dir (handy after authoring new labs)."""
    content_loader.reload()
    return {"status": "reloaded", "tracks": len(content_loader.list_tracks())}
