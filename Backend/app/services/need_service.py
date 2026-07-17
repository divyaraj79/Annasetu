from uuid import UUID

from sqlalchemy.orm import Session

from app.models.need import Need
from app.schemas.need import NeedCreate, NeedUpdate


class NeedService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, need_data: NeedCreate) -> Need:
        need = Need(**need_data.model_dump())
        self.db.add(need)
        self.db.commit()
        self.db.refresh(need)
        return need

    def get_by_id(self, need_id: UUID) -> Need | None:
        return self.db.query(Need).filter(Need.id == need_id).first()

    def get_all(self) -> list[Need]:
        return self.db.query(Need).all()

    def update(self, need: Need, need_data: NeedUpdate) -> Need:
        for field, value in need_data.model_dump(exclude_unset=True).items():
            setattr(need, field, value)
        self.db.commit()
        self.db.refresh(need)
        return need

    def delete(self, need: Need) -> None:
        self.db.delete(need)
        self.db.commit()
