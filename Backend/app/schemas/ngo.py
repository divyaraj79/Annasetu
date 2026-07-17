from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NGOCreate(BaseModel):
    user_id: UUID
    ngo_name: str
    phone: str
    address: str
    latitude: float | None = None
    longitude: float | None = None
    verified: bool = False


class NGOUpdate(BaseModel):
    user_id: UUID | None = None
    ngo_name: str | None = None
    phone: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    verified: bool | None = None
    is_deleted: bool | None = None


class NGOResponse(BaseModel):
    id: UUID
    user_id: UUID
    ngo_name: str
    phone: str
    address: str
    latitude: float | None = None
    longitude: float | None = None
    verified: bool
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
