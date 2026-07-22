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

        if not ranked_ngos:

            donation.status = DonationStatus.UNMATCHED

            # TODO:
            # Notify restaurant that no NGO
            # could be matched.

            return []
        
        matches = []

        for attempt_number, (ngo, score) in enumerate(
            ranked_ngos,
            start=1,
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

        donation.status = DonationStatus.MATCHING

        if matches:
            self.match_service.mark_as_notified(
                matches[0]
            )
            
            self.email_service.send_match_notification(
                donation,
                matches[0],
            )

        return matches