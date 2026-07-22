from uuid import UUID

from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.enums.roles import UserRole
from app.enums.verification_status import VerificationStatus


class RestaurantService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, restaurant_data: RestaurantCreate) -> Restaurant:
        # Check if user exists
        user = (
            self.db.query(User)
            .filter(User.id == restaurant_data.user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found.")

        if user.is_deleted:
            raise ValueError("User has been deleted!")

        # Check if user account is active
        if not user.is_active:
            raise ValueError("Inactive users cannot create a restaurant profile.")

        # Check user role
        if user.role != UserRole.RESTAURANT:
            raise ValueError("Only restaurant users can create a restaurant profile.")

        # Check if user already owns a restaurant
        existing_restaurant = (
            self.db.query(Restaurant)
            .filter(Restaurant.user_id == restaurant_data.user_id)
            .first()
        )

        if existing_restaurant:
            raise ValueError("Restaurant profile already exists for this user.")

        restaurant = Restaurant(
            **restaurant_data.model_dump(),
            verification_status=VerificationStatus.PENDING
        )

        # TODO:
        # Geocode the address here and automatically populate
        # latitude and longitude before saving.

        self.db.add(restaurant)
        self.db.flush()
        self.db.refresh(restaurant)

        return restaurant

    def get_by_id(self, restaurant_id: UUID) -> Restaurant | None:    
        return (
            self.db.query(Restaurant)
            .filter(
                Restaurant.id == restaurant_id,
                Restaurant.is_deleted == False,
            )
            .first()
        )
    
    def get_by_email(
        self,
        email: str,
    ) -> Restaurant | None:

        return (
            self.db.query(Restaurant)
            .join(User)
            .filter(
                User.email == email,
                User.is_deleted == False,
                Restaurant.is_deleted == False,
                Restaurant.verification_status
                == VerificationStatus.APPROVED,
            )
            .first()
        )

    def get_all(self) -> list[Restaurant]:
        return (
            self.db.query(Restaurant)
            .filter(Restaurant.is_deleted == False)
            .all()
        )

    def update(
        self,
        restaurant: Restaurant,
        restaurant_data: RestaurantUpdate
        ) -> Restaurant:

        # TODO:
        # After authentication is implemented,
        # validate that only the restaurant owner
        # (or an admin) can update this profile.
        #
        # If the address changes,
        # automatically geocode the new address
        # and update latitude & longitude.

        if restaurant.is_deleted:
            raise ValueError(
                "Deleted restaurants cannot be updated."
            )

        update_data = restaurant_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(restaurant, field, value)

        self.db.flush()
        self.db.refresh(restaurant)

        return restaurant
    
    def get_pending(self) -> list[Restaurant]:
        return (
            self.db.query(Restaurant)
            .filter(
                Restaurant.is_deleted == False,
                Restaurant.verification_status == VerificationStatus.PENDING,
            )
            .all()
        )

    def delete(
        self,
        restaurant: Restaurant,
    ) -> None:

        if restaurant.is_deleted:
            raise ValueError(
                "Restaurant is already deleted."
            )

        restaurant.is_deleted = True
        restaurant.user.is_deleted = True

        for donation in restaurant.donations:
            donation.is_deleted = True

            for donation_item in donation.donation_items:
                donation_item.is_deleted = True

            for match in donation.matches:
                match.is_deleted = True

        self.db.flush()

        self.db.refresh(restaurant)
