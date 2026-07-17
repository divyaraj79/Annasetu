from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ngo import NGO
from app.schemas.ngo import NGOCreate, NGOUpdate


class NGOService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, ngo_data: NGOCreate) -> NGO:
        ngo = NGO(**ngo_data.model_dump())
        self.db.add(ngo)
        self.db.commit()
        self.db.refresh(ngo)
        return ngo

    def get_by_id(self, ngo_id: UUID) -> NGO | None:
        return self.db.query(NGO).filter(NGO.id == ngo_id).first()

    def get_all(self) -> list[NGO]:
        return self.db.query(NGO).all()

    def update(self, ngo: NGO, ngo_data: NGOUpdate) -> NGO:
        for field, value in ngo_data.model_dump(exclude_unset=True).items():
            setattr(ngo, field, value)
        self.db.commit()
        self.db.refresh(ngo)
        return ngo

    def delete(self, ngo: NGO) -> None:
        self.db.delete(ngo)
        self.db.commit()
