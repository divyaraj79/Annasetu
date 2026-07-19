from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.roles import UserRole


class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    role: UserRole


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str| None = None


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime | None = None
    phone: str

    model_config = ConfigDict(from_attributes=True)
