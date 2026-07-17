from uuid import UUID

from sqlalchemy.orm import Session

from app.models.match import Match
from app.schemas.match import MatchCreate, MatchUpdate


class MatchService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, match_data: MatchCreate) -> Match:
        match = Match(**match_data.model_dump())
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match

    def get_by_id(self, match_id: UUID) -> Match | None:
        return self.db.query(Match).filter(Match.id == match_id).first()

    def get_all(self) -> list[Match]:
        return self.db.query(Match).all()

    def update(self, match: Match, match_data: MatchUpdate) -> Match:
        for field, value in match_data.model_dump(exclude_unset=True).items():
            setattr(match, field, value)
        self.db.commit()
        self.db.refresh(match)
        return match

    def delete(self, match: Match) -> None:
        self.db.delete(match)
        self.db.commit()
