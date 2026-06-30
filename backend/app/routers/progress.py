"""Progress tracking, XP/level awards, streaks, and badges."""
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import badges as badge_defs
from .. import content_loader
from ..auth import get_current_user
from ..database import get_db
from ..models import Progress, User, UserBadge
from ..schemas import BadgeOut, ProgressOut, StatsOut

router = APIRouter(prefix="/progress", tags=["progress"])

# 500 XP per level (simple, predictable curve).
XP_PER_LEVEL = 500


def level_for_xp(xp: int) -> int:
    return max(1, xp // XP_PER_LEVEL + 1)


def _update_streak(user: User) -> None:
    """Bump the daily streak based on today's activity (UTC date)."""
    today = datetime.now(timezone.utc).date()
    last = (
        date.fromisoformat(user.last_active_date)
        if user.last_active_date
        else None
    )
    if last == today:
        return  # already counted today
    if last == today - timedelta(days=1):
        user.streak_days += 1
    else:
        user.streak_days = 1
    user.last_active_date = today.isoformat()


async def _award_badges(db: AsyncSession, user: User) -> None:
    """Persist any newly-earned badges for the user."""
    result = await db.execute(select(Progress).where(Progress.user_id == user.id))
    rows = result.scalars().all()
    completed = [p for p in rows if p.status == "completed"]
    ctx = badge_defs.BadgeContext(
        completed_labs=sum(1 for p in completed if p.item_type == "lab"),
        completed_projects=sum(1 for p in completed if p.item_type == "project"),
        distinct_tracks=len({_track_of(p.item_id) for p in completed}),
        level=user.level,
        streak_days=user.streak_days,
    )
    qualified = set(badge_defs.evaluate(ctx))
    existing = await db.execute(
        select(UserBadge.badge_slug).where(UserBadge.user_id == user.id)
    )
    have = set(existing.scalars().all())
    for slug in qualified - have:
        db.add(UserBadge(user_id=user.id, badge_slug=slug))


def _track_of(item_id: str) -> str:
    lab = content_loader.get_lab(item_id)
    return lab.track if lab else item_id


async def record_completion(
    db: AsyncSession, user: User, item_type: str, item_id: str, score: int
) -> Progress:
    """Upsert progress, award XP/streak/badges the first time completed."""
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
    row.score = max(row.score or 0, score)  # score is None on a brand-new row
    row.completed_at = datetime.now(timezone.utc)

    if newly_completed:
        user.xp += score
        user.level = level_for_xp(user.xp)
    _update_streak(user)
    await db.flush()
    await _award_badges(db, user)

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


@router.get("/stats", response_model=StatsOut)
async def my_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user.id, Progress.status == "completed"
        )
    )
    completed = result.scalars().all()
    badge_rows = await db.execute(
        select(UserBadge).where(UserBadge.user_id == user.id)
    )
    return StatsOut(
        xp=user.xp,
        level=user.level,
        xp_into_level=user.xp % XP_PER_LEVEL,
        xp_per_level=XP_PER_LEVEL,
        completed=len(completed),
        streak_days=user.streak_days,
        badges_earned=len(badge_rows.scalars().all()),
    )


@router.get("/badges", response_model=list[BadgeOut])
async def my_badges(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = await db.execute(select(UserBadge).where(UserBadge.user_id == user.id))
    earned = {b.badge_slug: b.awarded_at for b in rows.scalars().all()}
    return [
        BadgeOut(
            slug=b.slug,
            title=b.title,
            description=b.description,
            earned=b.slug in earned,
            awarded_at=earned.get(b.slug),
        )
        for b in badge_defs.BADGES
    ]
