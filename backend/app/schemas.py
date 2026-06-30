"""Pydantic request/response models."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ─── Auth ─────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    username: str
    xp: int
    level: int


# ─── Catalog (loaded from disk) ───────────────────────────
class TrackOut(BaseModel):
    slug: str
    title: str
    level: str
    order_index: int
    description: str = ""
    lab_count: int = 0
    project_count: int = 0


class LabSummary(BaseModel):
    id: str
    track: str
    slug: str
    title: str
    level: str
    type: str = "lab"
    estimated_minutes: int
    points: int
    prerequisites: list[str] = []


class LabDetail(LabSummary):
    image: str
    theory_html: str = ""
    instructions_html: str = ""
    has_solution: bool = False


# ─── Progress ─────────────────────────────────────────────
class ProgressOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    item_type: str
    item_id: str
    status: str
    score: int
    completed_at: datetime | None = None


# ─── Lab sessions ─────────────────────────────────────────
class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    lab_id: str
    status: str
    started_at: datetime
    expires_at: datetime | None = None
    ws_url: str = ""


class CheckStep(BaseModel):
    name: str
    passed: bool
    message: str = ""


class CheckResult(BaseModel):
    passed: bool
    score: int
    steps: list[CheckStep]
    raw_output: str = ""


# ─── Editor / files ───────────────────────────────────────
class FileEntry(BaseModel):
    name: str
    type: str  # dir | file
    path: str


class FileContent(BaseModel):
    path: str
    content: str


class WriteFileRequest(BaseModel):
    path: str
    content: str


# ─── Hints / solution ─────────────────────────────────────
class SolutionOut(BaseModel):
    solution_html: str


# ─── Skill tree ───────────────────────────────────────────
class SkillNode(BaseModel):
    id: str
    track: str
    title: str
    level: str
    type: str = "lab"  # lab | project
    points: int
    prerequisites: list[str] = []
    status: str  # locked | available | completed


# ─── Badges ───────────────────────────────────────────────
class BadgeOut(BaseModel):
    slug: str
    title: str
    description: str
    earned: bool
    awarded_at: datetime | None = None


# ─── Gamification summary ─────────────────────────────────
class StatsOut(BaseModel):
    xp: int
    level: int
    xp_into_level: int
    xp_per_level: int
    completed: int
    streak_days: int
    badges_earned: int
