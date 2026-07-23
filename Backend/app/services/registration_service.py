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

from app.enums.verification_status import VerificationStatus
from app.models.restaurant import Restaurant
from app.models.ngo import NGO

from uuid import UUID

from app.automation.email_service import EmailService


class RegistrationService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()

    def register(self, registration_data: RegistrationRequest):
        user_service = UserService(self.db)
        restaurant_service = RestaurantService(self.db)
        ngo_service = NGOService(self.db)

        if registration_data.role == UserRole.ADMIN:
            raise ValueError(
                "Admin registration is not allowed."
            )
        
        hashed_password = hash_password(
            registration_data.password
        )

        # user_service = UserService(self.db)

        try:
            user = user_service.create(
                UserCreate(
                    name=registration_data.name,
                    email=registration_data.email,
                    phone=registration_data.phone,
                    role=registration_data.role,
                    password_hash=hashed_password,
                )
            )

            if registration_data.role == UserRole.RESTAURANT:
                restaurant_service.create(
                    RestaurantCreate(
                        user_id=user.id,
                        restaurant_name=registration_data.organization_name,
                        address=registration_data.address,
                    )
                )

            elif registration_data.role == UserRole.NGO:
                ngo_service.create(
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

    def get_pending_restaurants(self) -> list[Restaurant]:
        restaurant_service = RestaurantService(self.db)

        return restaurant_service.get_pending()
    
    def get_pending_ngos(self) -> list[NGO]:
        ngo_service = NGOService(self.db)

        return ngo_service.get_pending()
    
    def approve_restaurant_registration(
        self,
        restaurant_id: UUID,
    ) -> Restaurant:
        restaurant_service = RestaurantService(self.db)

        restaurant = restaurant_service.get_by_id(restaurant_id)

        if not restaurant:
            raise ValueError("Restaurant not found.")

        if restaurant.verification_status != VerificationStatus.PENDING:
            raise ValueError("Only pending restaurants can be approved.")

        try:
            restaurant.verification_status = VerificationStatus.APPROVED

            self.email_service.send_restaurant_registration_approval(
                restaurant,
            )

            self.db.commit()
            self.db.refresh(restaurant)

            return restaurant

        except Exception:
            self.db.rollback()
            raise
    
    def approve_ngo_registration(
        self,
        ngo_id: UUID,
    ) -> NGO:
        ngo_service = NGOService(self.db)

        ngo = ngo_service.get_by_id(ngo_id)

        if not ngo:
            raise ValueError("NGO not found.")

        if ngo.verification_status != VerificationStatus.PENDING:
            raise ValueError("Only pending NGOs can be approved.")

        try:
            ngo.verification_status = VerificationStatus.APPROVED

            self.email_service.send_ngo_registration_approval(
                ngo,
            )

            self.db.commit()
            self.db.refresh(ngo)

            return ngo

        except Exception:
            self.db.rollback()
            raise
    
    def _delete_registration(self, organization, user):
        try:
            self.db.delete(organization)
            self.db.flush()

            self.db.delete(user)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
    
    def reject_restaurant_registration(
        self,
        restaurant_id: UUID,
    ) -> None:
        restaurant_service = RestaurantService(self.db)

        restaurant = restaurant_service.get_by_id(restaurant_id)

        if not restaurant:
            raise ValueError("Restaurant not found.")

        if restaurant.verification_status != VerificationStatus.PENDING:
            raise ValueError("Only pending restaurant registrations can be rejected.")


        user = restaurant.user
        self._delete_registration(restaurant, user)

    def reject_ngo_registration(
        self,
        ngo_id: UUID,
    ) -> None:
        ngo_service = NGOService(self.db)

        ngo = ngo_service.get_by_id(ngo_id)

        if not ngo:
            raise ValueError("NGO not found.")

        if ngo.verification_status != VerificationStatus.PENDING:
            raise ValueError("Only pending NGO registrations can be rejected.")

        user = ngo.user
        self._delete_registration(ngo, user)