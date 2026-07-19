from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.verification_status import VerificationStatus


class NGOCreate(BaseModel):
    user_id: UUID
    ngo_name: str
    address: str


class NGOUpdate(BaseModel):
    ngo_name: str | None = None
    address: str | None = None


class NGOResponse(BaseModel):
    id: UUID
    user_id: UUID
    ngo_name: str
    address: str
    latitude: float | None = None
    longitude: float | None = None
    verification_status: VerificationStatus
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
