from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    # def create(self, user_data: UserCreate) -> User:
    #     user = User(**user_data.model_dump())
    #     self.db.add(user)
    #     self.db.flush()
    #     self.db.refresh(user)
    #     return user


    def create(self, user_data: UserCreate) -> User:
        existing_user = (
            self.db.query(User)
            .filter(
                or_(
                    User.email == user_data.email,
                    User.phone == user_data.phone,
                )
            )
            .first()
        )

        if existing_user:
            raise ValueError("Email or phone already registered.")

        user = User(**user_data.model_dump())

        self.db.add(user)

        self.db.flush()

        self.db.refresh(user)

        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def update(self, user: User, user_data: UserUpdate) -> User:
        update_data = user_data.model_dump(exclude_unset=True)

        if "email" in update_data:

            existing = (
                self.db.query(User)
                .filter(
                    User.email == update_data["email"],
                    User.id != user.id,
                )
                .first()
            )

            if existing:
                raise ValueError("Email already exists.")

        if "phone" in update_data:

            existing = (
                self.db.query(User)
                .filter(
                    User.phone == update_data["phone"],
                    User.id != user.id,
                )
                .first()
            )

            if existing:
                raise ValueError("Phone already exists.")

        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.flush()

        self.db.refresh(user)

        return user


    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.flush()
