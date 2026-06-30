"""Badge definitions + award evaluation.

Definitions live in code (not the DB) so they're versionable. Each badge has a
predicate over a user's aggregate stats; `evaluate` returns the slugs a user
currently qualifies for, and the progress router persists new awards.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Badge:
    slug: str
    title: str
    description: str
    predicate: Callable[["BadgeContext"], bool]


@dataclass
class BadgeContext:
    completed_labs: int
    completed_projects: int
    distinct_tracks: int
    level: int
    streak_days: int


BADGES: list[Badge] = [
    Badge("first-steps", "First Steps", "Complete your first lab",
          lambda c: c.completed_labs >= 1),
    Badge("getting-warm", "Getting Warm", "Complete 5 labs",
          lambda c: c.completed_labs >= 5),
    Badge("lab-rat", "Lab Rat", "Complete 15 labs",
          lambda c: c.completed_labs >= 15),
    Badge("builder", "Builder", "Complete your first project",
          lambda c: c.completed_projects >= 1),
    Badge("portfolio", "Portfolio", "Complete 5 projects",
          lambda c: c.completed_projects >= 5),
    Badge("explorer", "Explorer", "Touch 3 different tracks",
          lambda c: c.distinct_tracks >= 3),
    Badge("polyglot", "Polyglot", "Touch 6 different tracks",
          lambda c: c.distinct_tracks >= 6),
    Badge("level-5", "Rising Star", "Reach level 5",
          lambda c: c.level >= 5),
    Badge("level-10", "DevOps Pro", "Reach level 10",
          lambda c: c.level >= 10),
    Badge("streak-3", "On a Roll", "Keep a 3-day streak",
          lambda c: c.streak_days >= 3),
    Badge("streak-7", "Unstoppable", "Keep a 7-day streak",
          lambda c: c.streak_days >= 7),
]

BY_SLUG = {b.slug: b for b in BADGES}


def evaluate(ctx: BadgeContext) -> list[str]:
    """Return slugs of all badges the user currently qualifies for."""
    return [b.slug for b in BADGES if b.predicate(ctx)]
