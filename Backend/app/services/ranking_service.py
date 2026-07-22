from app.models.donation import Donation
from app.models.ngo import NGO
from app.models.need import Need

# from app.enums.verification_status import VerificationStatus
from app.enums.status import DonationStatus
from app.enums.urgency import Urgency

CATEGORY_MATCH_SCORE = 50
VEGETARIAN_MATCH_SCORE = 30
URGENCY_SCORES = {
    Urgency.LOW: 10,
    Urgency.MEDIUM: 20,
    Urgency.HIGH: 30,
}

class RankingService:

    def rank_ngos(
        self,
        donation: Donation,
        ngos: list[NGO],
    ) -> list[tuple[NGO, float]]:
        """
        Rank NGOs for a donation using their active needs.
        """

        ranked_ngos = []

        for ngo in ngos:

            score = self._calculate_score(
                donation,
                ngo,
            )

            if score <= 0:
                continue

            ranked_ngos.append(
                (
                    ngo,
                    score,
                )
            )

        ranked_ngos.sort(
            key=lambda candidate: candidate[1],
            reverse=True,
        )

        return ranked_ngos
    

    def _calculate_score(
        self,
        donation: Donation,
        ngo: NGO,
    ) -> float:

        score = 0.0

        active_needs = [
            need
            for need in ngo.needs
            if (
                not need.is_deleted
                and need.status == DonationStatus.CREATED
            )
        ]

        if not active_needs:
            return score

        best_need = max(
            (
                self._score_need(
                    donation,
                    need,
                )
                for need in active_needs
            ),
            default=0.0,
        )

        score += best_need

        return score


    def _score_need(
        self,
        donation: Donation,
        need: Need,
    ) -> float:

        score = 0.0

        if (
            donation.food_category
            == need.preferred_category
        ):
            score += CATEGORY_MATCH_SCORE

        if (
            not need.vegetarian_only
            or donation.is_vegetarian
        ):
            score += VEGETARIAN_MATCH_SCORE

        score += URGENCY_SCORES.get(need.urgency, 0)

        # TODO:
        # Add distance scoring.

        return score
