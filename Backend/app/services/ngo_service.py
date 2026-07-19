from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ngo import NGO
from app.models.user import User
from app.schemas.ngo import NGOCreate, NGOUpdate
from app.enums.roles import UserRole
from app.enums.verification_status import VerificationStatus


class NGOService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, ngo_data: NGOCreate) -> NGO:
        # Check if user exists
        user = (
            self.db.query(User)
            .filter(User.id == ngo_data.user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found.")

        # Check if user account is active
        if not user.is_active:
            raise ValueError("Inactive users cannot create an NGO profile.")

        # Check user role
        if user.role != UserRole.NGO:
            raise ValueError("Only NGO users can create an NGO profile.")

        # Check if user already owns an NGO
        existing_ngo = (
            self.db.query(NGO)
            .filter(NGO.user_id == ngo_data.user_id)
            .first()
        )

        if existing_ngo:
            raise ValueError("NGO profile already exists for this user.")

        ngo = NGO(
            **ngo_data.model_dump(),
            verification_status=VerificationStatus.PENDING
        )

        # TODO:
        # Geocode the address here and automatically populate
        # latitude and longitude before saving.

        self.db.add(ngo)
        self.db.flush()
        self.db.refresh(ngo)

        return ngo

    def get_by_id(self, ngo_id: UUID) -> NGO | None:
        return self.db.query(NGO).filter(NGO.id == ngo_id).first()

    def get_all(self) -> list[NGO]:
        return self.db.query(NGO).all()

    def update(
        self,
        ngo: NGO,
        ngo_data: NGOUpdate
    ) -> NGO:
        # TODO:
        # After authentication is implemented,
        # validate that only the NGO owner
        # (or an admin) can update this profile.
        #
        # If the address changes,
        # automatically geocode the new address
        # and update latitude & longitude.

        update_data = ngo_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(ngo, field, value)

        self.db.flush()
        self.db.refresh(ngo)

        return ngo
        

    def delete(self, ngo: NGO) -> None:
        self.db.delete(ngo)
        self.db.flush()
