from uuid import UUID

from sqlalchemy.orm import Session

from app.models.need import Need
from app.models.ngo import NGO

from app.schemas.need import NeedCreate, NeedUpdate

from app.enums.status import DonationStatus
from app.enums.verification_status import VerificationStatus


class NeedService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, need_data: NeedCreate) -> Need:
        # Check NGO exists
        ngo = (
            self.db.query(NGO)
            .filter(NGO.id == need_data.ngo_id)
            .first()
        )

        if not ngo:
            raise ValueError("NGO not found.")

        # NGO must not be deleted
        if ngo.is_deleted:
            raise ValueError("NGO profile has been deleted.")

        # NGO must be approved
        if ngo.verification_status != VerificationStatus.APPROVED:
            raise ValueError("NGO is not approved.")

        # Quantity validation
        if need_data.quantity_required <= 0:
            raise ValueError("Quantity must be greater than zero.")

        need = Need(
            **need_data.model_dump(),
            status=DonationStatus.CREATED,
        )

        self.db.add(need)

        self.db.flush()

        self.db.refresh(need)

        return need

    def get_by_id(self, need_id: UUID) -> Need | None:
        return self.db.query(Need).filter(Need.id == need_id).first()

    def get_all(self) -> list[Need]:
        return self.db.query(Need).all()

    def update(
        self,
        need: Need,
        need_data: NeedUpdate,
    ) -> Need:

        # Completed needs cannot be modified
        if need.status == DonationStatus.COMPLETED:
            raise ValueError("Completed needs cannot be updated.")

        update_data = need_data.model_dump(exclude_unset=True)

        # Quantity validation
        if (
            "quantity_required" in update_data
            and update_data["quantity_required"] <= 0
        ):
            raise ValueError("Quantity must be greater than zero.")
        # TODO:
        # After authentication,
        # ensure only the owning NGO
        # (or admin)
        # can update this need.

        for field, value in update_data.items():
            setattr(need, field, value)

        self.db.flush()

        self.db.refresh(need)

        return need

    def delete(self, need: Need) -> None:
        self.db.delete(need)
        self.db.flush()
