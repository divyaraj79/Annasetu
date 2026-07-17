from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.match import MatchCreate, MatchResponse, MatchUpdate
from app.services.match_service import MatchService

router = APIRouter(prefix="/matches", tags=["matches"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    service = MatchService(db)
    return service.create(match)


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: UUID, db: Session = Depends(get_db)):
    service = MatchService(db)
    match = service.get_by_id(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match


@router.get("/", response_model=list[MatchResponse])
def get_matches(db: Session = Depends(get_db)):
    service = MatchService(db)
    return service.get_all()


@router.put("/{match_id}", response_model=MatchResponse)
def update_match(match_id: UUID, match_data: MatchUpdate, db: Session = Depends(get_db)):
    service = MatchService(db)
    match = service.get_by_id(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return service.update(match, match_data)


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: UUID, db: Session = Depends(get_db)):
    service = MatchService(db)
    match = service.get_by_id(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    service.delete(match)
    return None
