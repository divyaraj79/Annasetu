from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)

from app.enums.roles import UserRole


class RegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRole
    organization_name: str
    address: str

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
    def validate_email(
        cls,
        value: EmailStr,
    ) -> EmailStr:
        return value.strip().lower()

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

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ) -> str:
        if len(value) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        if len(value) > 20:
            raise ValueError(
                "Password cannot exceed 20 characters."
            )

        return value

    @field_validator("organization_name")
    @classmethod
    def validate_organization_name(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Organization name must contain at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Organization name cannot exceed 100 characters."
            )

        return value

    @field_validator("address")
    @classmethod
    def validate_address(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if len(value) < 5:
            raise ValueError(
                "Address must contain at least 5 characters."
            )

        if len(value) > 255:
            raise ValueError(
                "Address cannot exceed 255 characters."
            )

        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(
        cls,
        value: EmailStr,
    ) -> EmailStr:
        return value.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if len(value) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        if len(value) > 20:
            raise ValueError(
                "Password cannot exceed 20 characters."
            )

        return value


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"