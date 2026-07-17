from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.roles import UserRole


class UserCreate(BaseModel):
    name: str
    email: str
    role: UserRole
    is_active: bool = True


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
