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
