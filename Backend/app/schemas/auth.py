from pydantic import BaseModel, EmailStr

from app.enums.roles import UserRole


class RegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRole
    organization_name: str
    address: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
