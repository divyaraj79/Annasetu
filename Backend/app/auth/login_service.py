from sqlalchemy.orm import Session

from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token

from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)


class LoginService:
    def __init__(self, db: Session):
        self.db = db

    def login(
        self,
        login_data: LoginRequest,
    ) -> TokenResponse:

        user = (
            self.db.query(User)
            .filter(User.email == login_data.email)
            .first()
        )

        if not user:
            raise ValueError("Invalid email or password.")
        
        if not user.password_hash:
            raise ValueError("Invalid email or password.")
        
        if user.is_deleted:
            raise ValueError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            login_data.password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password.")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
            }
        )

        return TokenResponse(
            access_token=access_token,
        )