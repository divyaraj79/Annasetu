from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.ngo import NGO
from app.models.match import Match

from app.schemas.match import MatchCreate

from app.enums.verification_status import VerificationStatus
from app.enums.status import DonationStatus

from app.services.match_service import MatchService
from app.services.ranking_service import RankingService

from app.automation.email_service import EmailService

class MatchingService:

    def __init__(self, db: Session):
        self.db = db

        self.match_service = MatchService(db)
        self.ranking_service = RankingService()
        self.email_service = EmailService()

    def create_matches(
        self,
        donation: Donation,
    ) -> list[Match]:

        if donation.status not in (
            DonationStatus.CREATED,
            DonationStatus.MATCHING,
            DonationStatus.UNMATCHED,
        ):
            return []
        
        ngos = (
            self.db.query(NGO)
            .filter(
                NGO.is_deleted == False,
                NGO.verification_status == VerificationStatus.APPROVED,
            )
            .all()
        )

        ranked_ngos = self.ranking_service.rank_ngos(
            donation,
            ngos,
        )

        existing_matches = (
            self.db.query(Match)
            .filter(
                Match.donation_id == donation.id,
            )
            .count()
        )

        if not ranked_ngos:

            if existing_matches == 0:

                donation.status = DonationStatus.UNMATCHED

                self.email_service.send_donation_unmatched(
                    donation.restaurant,
                )

            return []
        
        matches = []

        # Never create a second Match row for the same NGO.
        # Existing rows (even soft-deleted declined ones)
        # preserve attempt history.
        existing_ngo_ids = {
            match.ngo_id
            for match in donation.matches
        }

        ranked_ngos = [
            (ngo, score)
            for ngo, score in ranked_ngos
                if ngo.id not in existing_ngo_ids
        ]

        
        existing_matches = (
            self.db.query(Match)
            .filter(
                Match.donation_id == donation.id,
            )
            .count()
        )

        start_attempt = existing_matches + 1

        for attempt_number, (ngo, score) in enumerate(
            ranked_ngos,
            start=start_attempt,
        ):
            match = self.match_service.create(
                MatchCreate(
                    donation_id=donation.id,
                    ngo_id=ngo.id,
                ),
                score=score,
                attempt_number=attempt_number,
            )

            matches.append(match)

        if donation.status == DonationStatus.CREATED:
            donation.status = DonationStatus.MATCHING

        return matches