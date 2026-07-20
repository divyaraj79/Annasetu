from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.match import MatchCreate, MatchResponse, MatchUpdate
from app.services.match_service import MatchService

from app.auth.dependencies import get_current_user, require_role

from app.models.user import User
from app.enums.roles import UserRole

from app.models.donation import Donation
from app.models.restaurant import Restaurant
from app.models.ngo import NGO

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(
    match: MatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    service = MatchService(db)

    try:
        created_match = service.create(match)

        db.commit()

        db.refresh(created_match)

        return created_match

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


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
def update_match(
    match_id: UUID,
    match_data: MatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MatchService(db)
    match = service.get_by_id(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    
    donation = (
        db.query(Donation)
        .filter(Donation.id == match.donation_id)
        .first()
    )

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == donation.restaurant_id)
        .first()
    )

    ngo = (
        db.query(NGO)
        .filter(NGO.id == match.ngo_id)
        .first()
    )

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != restaurant.user_id
        and current_user.id != ngo.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this match.",
        )

    try:
        updated_match = service.update(match, match_data)

        db.commit()

        db.refresh(updated_match)

        return updated_match

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(
    match_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MatchService(db)
    match = service.get_by_id(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    
    donation = (
        db.query(Donation)
        .filter(Donation.id == match.donation_id)
        .first()
    )

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == donation.restaurant_id)
        .first()
    )

    ngo = (
        db.query(NGO)
        .filter(NGO.id == match.ngo_id)
        .first()
    )

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != restaurant.user_id
        and current_user.id != ngo.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this match.",
        )

    try:
        service.delete(match)

        db.commit()

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise

    return None
