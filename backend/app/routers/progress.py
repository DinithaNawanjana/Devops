"""Progress tracking + XP/level awards."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..database import get_db
from ..models import Progress, User
from ..schemas import ProgressOut

router = APIRouter(prefix="/progress", tags=["progress"])

# 500 XP per level (simple, predictable curve).
XP_PER_LEVEL = 500


def level_for_xp(xp: int) -> int:
    return max(1, xp // XP_PER_LEVEL + 1)


async def record_completion(
    db: AsyncSession, user: User, item_type: str, item_id: str, score: int
) -> Progress:
    """Upsert progress and award XP the first time an item is completed."""
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user.id,
            Progress.item_type == item_type,
            Progress.item_id == item_id,
        )
    )
    row = result.scalar_one_or_none()
    newly_completed = row is None or row.status != "completed"

    if row is None:
        row = Progress(user_id=user.id, item_type=item_type, item_id=item_id)
        db.add(row)

    row.status = "completed"
    row.score = max(row.score, score)
    row.completed_at = datetime.now(timezone.utc)

    if newly_completed:
        user.xp += score
        user.level = level_for_xp(user.xp)

    await db.commit()
    await db.refresh(row)
    return row


@router.get("", response_model=list[ProgressOut])
async def my_progress(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Progress).where(Progress.user_id == user.id))
    return result.scalars().all()
