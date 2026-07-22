from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    field_validator,
)

from app.enums.roles import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    password_hash: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Name must contain at least 2 characters."
            )

        if len(value) > 60:
            raise ValueError(
                "Name cannot exceed 60 characters."
            )

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr) -> EmailStr:
        value = value.strip().lower()
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )

        return value


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str| None = None

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Name must contain at least 2 characters."
            )

        if len(value) > 60:
            raise ValueError(
                "Name cannot exceed 60 characters."
            )

        return value

    @field_validator("email")
    @classmethod
    def validate_email(
        cls,
        value: EmailStr | None,
    ) -> EmailStr | None:

        if value is None:
            return value

        value = value.strip().lower()

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )

        return value


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime | None = None
    phone: str

    model_config = ConfigDict(from_attributes=True)
