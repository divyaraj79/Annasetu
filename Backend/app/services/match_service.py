from uuid import UUID

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.donation import Donation
from app.models.ngo import NGO

from app.schemas.match import MatchCreate, MatchUpdate

from app.enums.status import DonationStatus, MatchStatus
from app.enums.verification_status import VerificationStatus

class MatchService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, match_data: MatchCreate) -> Match:
        # Check Donation exists
        donation = (
            self.db.query(Donation)
            .filter(Donation.id == match_data.donation_id)
            .first()
        )

        if not donation:
            raise ValueError("Donation not found.")

        # Donation should not be completed
        if donation.status == DonationStatus.COMPLETED:
            raise ValueError("Completed donations cannot be matched.")

        # Donation should not be cancelled
        if donation.status == DonationStatus.CANCELLED:
            raise ValueError("Cancelled donations cannot be matched.")

        # Donation should not be expired
        if donation.status == DonationStatus.EXPIRED:
            raise ValueError("Expired donations cannot be matched.")

        # Check NGO exists
        ngo = (
            self.db.query(NGO)
            .filter(NGO.id == match_data.ngo_id)
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

        # Prevent duplicate match
        existing_match = (
            self.db.query(Match)
            .filter(
                Match.donation_id == match_data.donation_id,
                Match.ngo_id == match_data.ngo_id,
            )
            .first()
        )

        if existing_match:
            raise ValueError(
                "A match already exists for this donation and NGO."
            )

        # TODO:
        # Calculate actual distance using
        # Donation and NGO coordinates.
        distance_km = 0.0

        match = Match(
            donation_id=match_data.donation_id,
            ngo_id=match_data.ngo_id,
            score=None,
            distance_km=distance_km,
            status=MatchStatus.PENDING,
            attempt_number=1,
            match_reason=None,
        )

        self.db.add(match)

        self.db.flush()

        self.db.refresh(match)

        return match

    def get_by_id(self, match_id: UUID) -> Match | None:
        return (
            self.db.query(Match)
            .filter(Match.id == match_id)
            .first()
        )

    def get_all(self) -> list[Match]:
        return self.db.query(Match).all()

    def update(
        self,
        match: Match,
        match_data: MatchUpdate,
    ) -> Match:

        update_data = match_data.model_dump(exclude_unset=True)

        # Completed matches cannot be modified
        if match.status == MatchStatus.COMPLETED:
            raise ValueError("Completed matches cannot be updated.")

        # TODO:
        # After authentication,
        # ensure only the assigned NGO
        # (or admin)
        # can update this match.

        for field, value in update_data.items():
            setattr(match, field, value)

        self.db.flush()

        self.db.refresh(match)

        return match

    def delete(self, match: Match) -> None:
        self.db.delete(match)
        self.db.flush()
