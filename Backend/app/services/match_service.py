from math import asin, cos, radians, sin, sqrt
from uuid import UUID

from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.models.match import Match
from app.models.donation import Donation
from app.models.ngo import NGO
from app.models.need import Need

from app.schemas.match import MatchCreate, MatchUpdate

from app.enums.status import DonationStatus, MatchStatus
from app.enums.verification_status import VerificationStatus

class MatchService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, match_data: MatchCreate, score: float | None = None, attempt_number: int = 1) -> Match:
        # Check Donation exists
        donation = (
            self.db.query(Donation)
            .filter(Donation.id == match_data.donation_id)
            .first()
        )

        if not donation:
            raise ValueError("Donation not found.")
        
        if donation.is_deleted:
            raise ValueError("Donation has been deleted.")

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
                "A match already exists for this donation andNGO."
            )

        distance_km = self._distance_km(donation, ngo)
        if distance_km is None:
            raise ValueError("Both the donation and NGO must have location coordinates.")

        match = Match(
            donation_id=match_data.donation_id,
            ngo_id=match_data.ngo_id,
            score=score if score is not None else self._match_score(donation, ngo, distance_km),
            distance_km=distance_km,
            status=MatchStatus.PENDING,
            notified_at=None,
            attempt_number=attempt_number,
            match_reason=f"Nearby food match at {distance_km:.1f} km.",
        )

        self.db.add(match)

        self.db.flush()

        self.db.refresh(match)

        return match

    def create_nearby_matches(self, donation: Donation) -> list[Match]:
        needs = (
            self.db.query(Need)
            .filter(Need.is_deleted == False)
            .all()
        )
        matches = []
        matched_ngo_ids = set()

        for need in needs:
            if need.ngo_id in matched_ngo_ids:
                continue
            if need.preferred_category != donation.food_category:
                continue
            if need.vegetarian_only and not donation.is_vegetarian:
                continue

            ngo = need.ngo
            if ngo.is_deleted or ngo.verification_status != VerificationStatus.APPROVED:
                continue

            distance_km = self._distance_km(donation, ngo)
            if distance_km is None:
                continue

            existing_match = (
                self.db.query(Match)
                .filter(
                    Match.donation_id == donation.id,
                    Match.ngo_id == ngo.id,
                )
                .first()
            )
            if existing_match:
                continue

            match = Match(
                donation_id=donation.id,
                ngo_id=ngo.id,
                score=self._match_score(donation, ngo, distance_km),
                distance_km=distance_km,
                status=MatchStatus.PENDING,
                attempt_number=1,
                match_reason=(
                    f"{donation.food_category.value.replace('_', ' ')} food is "
                    f"available {distance_km:.1f} km away."
                ),
            )
            self.db.add(match)
            matches.append(match)
            matched_ngo_ids.add(need.ngo_id)

        return matches

    @staticmethod
    def _distance_km(donation: Donation, ngo: NGO) -> float |None:
        coordinates = (
            donation.latitude,
            donation.longitude,
            ngo.latitude,
            ngo.longitude,
        )
        if any(value is None for value in coordinates):
            return None

        latitude_1, longitude_1, latitude_2, longitude_2 = map(radians, coordinates)
        latitude_delta = latitude_2 - latitude_1
        longitude_delta = longitude_2 - longitude_1
        haversine = (
            sin(latitude_delta / 2) ** 2
            + cos(latitude_1) * cos(latitude_2) * sin(longitude_delta / 2) ** 2
        )
        return round(6371 * 2 * asin(sqrt(haversine)), 2)

    @staticmethod
    def _match_score(donation: Donation, ngo: NGO, distance_km: float) -> float:
        quantity_score = min(donation.quantity / 100, 1) * 20
        distance_score = max(0, 60 - distance_km) / 60 * 80
        return round(quantity_score + distance_score, 2)

    def get_by_id(self, match_id: UUID) -> Match | None:
        return (
            self.db.query(Match)
            .filter(
                Match.id == match_id,
                Match.is_deleted == False,
            )
            .first()
        )

    def get_all(self) -> list[Match]:
        return (
            self.db.query(Match)
            .filter(Match.is_deleted == False)
            .all()
        )

    def update(
        self,
        match: Match,
        match_data: MatchUpdate,
    ) -> Match:
        
        if match.is_deleted:
            raise ValueError(
                "Deleted matches cannot be updated."
            )

        update_data = match_data.model_dump(exclude_unset=True)

        # Completed matches cannot be modified
        if match.status == MatchStatus.COMPLETED:
            raise ValueError("Completed matches cannot be updated.")

        if "status" in update_data:
            allowed_statuses = {
                MatchStatus.PENDING: {MatchStatus.INTERESTED,MatchStatus.REJECTED},
                MatchStatus.INTERESTED: {MatchStatus.ACCEPTED, MatchStatus.REJECTED},
                MatchStatus.ACCEPTED: {MatchStatus.COMPLETED},
            }
            allowed = allowed_statuses.get(match.status, set())
            if update_data["status"] not in allowed:
                raise ValueError("This match status change isnot allowed.")

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

    def delete(
        self,
        match: Match,
    ) -> None:

        if match.is_deleted:
            raise ValueError(
                "Match is already deleted."
            )

        match.is_deleted = True

        self.db.flush()

        self.db.refresh(match)

    # --------------------------------------------------
    # Workflow Actions
    # --------------------------------------------------

    def mark_as_notified(
        self,
        match: Match,
    ) -> Match:

        if match.is_deleted:
            raise ValueError(
                "Deleted matches cannot be notified."
            )

        if match.status != MatchStatus.PENDING:
            raise ValueError(
                "Only pending matches can be notified."
            )

        match.status = MatchStatus.NOTIFIED
        match.notified_at = datetime.now(timezone.utc)

        self.db.flush()
        self.db.refresh(match)

        return match

    def mark_as_accepted(
        self,
        match: Match,
    ) -> Match:

        if match.is_deleted:
            raise ValueError(
                "Deleted matches cannot be accepted."
            )

        if match.status != MatchStatus.NOTIFIED:
            raise ValueError(
                "Only notified matches can be accepted."
            )

        match.status = MatchStatus.ACCEPTED
        match.responded_at = datetime.now(timezone.utc)

        self.db.flush()
        self.db.refresh(match)

        return match

    def mark_as_declined(
        self,
        match: Match,
        reason: str | None,
    ) -> Match:

        if match.is_deleted:
            raise ValueError(
                "Deleted matches cannot be declined."
            )

        if match.status != MatchStatus.NOTIFIED:
            raise ValueError(
                "Only notified matches can be declined."
            )

        if reason is None:
            reason = "No reason provided."

        else:
            reason = reason.strip()
            if not reason:
                reason = "No reason provided."

        match.status = MatchStatus.DECLINED
        match.responded_at = datetime.now(timezone.utc)
        match.match_reason = reason
        match.is_deleted = True

        self.db.flush()
        self.db.refresh(match)

        return match

    def mark_as_completed(
        self,
        match: Match,
    ) -> Match:

        if match.is_deleted:
            raise ValueError(
                "Deleted matches cannot be completed."
            )

        if match.status != MatchStatus.ACCEPTED:
            raise ValueError(
                "Only accepted matches can be completed."
            )

        match.status = MatchStatus.COMPLETED

        self.db.flush()
        self.db.refresh(match)

        return match