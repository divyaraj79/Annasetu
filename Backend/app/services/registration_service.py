from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.enums.roles import UserRole
from app.schemas.auth import RegistrationRequest
from app.schemas.ngo import NGOCreate
from app.schemas.restaurant import RestaurantCreate
from app.schemas.user import UserCreate
from app.services.ngo_service import NGOService
from app.services.restaurant_service import RestaurantService
from app.services.user_service import UserService


class RegistrationService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, registration_data: RegistrationRequest):
        if registration_data.role == UserRole.ADMIN:
            raise ValueError(
                "Admin registration is not allowed."
            )
        
        hashed_password = hash_password(
            registration_data.password
        )

        user_service = UserService(self.db)

        try:
            user = user_service.create(
                UserCreate(
                    name=registration_data.name,
                    email=registration_data.email,
                    phone=registration_data.phone,
                    role=registration_data.role,
                )
            )

            user.password_hash = hashed_password

            if registration_data.role == UserRole.RESTAURANT:
                RestaurantService(self.db).create(
                    RestaurantCreate(
                        user_id=user.id,
                        restaurant_name=registration_data.organization_name,
                        address=registration_data.address,
                    )
                )

            elif registration_data.role == UserRole.NGO:
                NGOService(self.db).create(
                    NGOCreate(
                        user_id=user.id,
                        ngo_name=registration_data.organization_name,
                        address=registration_data.address,
                    )
                )

            self.db.commit()

            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise