from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.status import MatchStatus


class MatchCreate(BaseModel):
    donation_id: UUID
    ngo_id: UUID
    score: float | None = None
    status: MatchStatus | None = None
    attempt_number: int
    match_reason: str | None = None


class MatchUpdate(BaseModel):
    donation_id: UUID | None = None
    ngo_id: UUID | None = None
    score: float | None = None
    status: MatchStatus | None = None
    attempt_number: int | None = None
    responded_at: datetime | None = None
    match_reason: str | None = None


class MatchResponse(BaseModel):
    id: UUID
    donation_id: UUID
    ngo_id: UUID
    score: float | None = None
    status: MatchStatus
    attempt_number: int
    matched_at: datetime | None = None
    responded_at: datetime | None = None
    match_reason: str | None = None

    model_config = ConfigDict(from_attributes=True)
