from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.need import NeedCreate, NeedResponse, NeedUpdate
from app.services.need_service import NeedService

from app.auth.dependencies import (
    get_current_user,
)

from app.models.user import User
from app.enums.roles import UserRole
from app.models.ngo import NGO

router = APIRouter(prefix="/needs", tags=["needs"])

@router.post("/", response_model=NeedResponse, status_code=status.HTTP_201_CREATED)
def create_need(
    need: NeedCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)    
):
    service = NeedService(db)

    ngo = (
        db.query(NGO)
        .filter(NGO.id == need.ngo_id)
        .first()
    )

    if not ngo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NGO not found.",
        )
    
    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != ngo.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to create this need.",
        )

    try:
        need = service.create(need)

        db.commit()

        db.refresh(need)

        return need

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.get("/{need_id}", response_model=NeedResponse)
def get_need(need_id: UUID, db: Session = Depends(get_db)):
    service = NeedService(db)
    need = service.get_by_id(need_id)
    if not need:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Need not found")
    return need


@router.get("/", response_model=list[NeedResponse])
def get_needs(db: Session = Depends(get_db)):
    service = NeedService(db)
    return service.get_all()


@router.put("/{need_id}", response_model=NeedResponse)
def update_need(
    need_id: UUID, 
    need_data: NeedUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NeedService(db)
    need = service.get_by_id(need_id) 

    if not need:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Need not found")
    
    ngo = (
        db.query(NGO)
        .filter(NGO.id == need.ngo_id)
        .first()
    )

    if not ngo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NGO not found.",
        )

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != ngo.user_id
    ): 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this need.",
        )
    
    try:
        updated_need = service.update(need, need_data)

        db.commit()

        db.refresh(updated_need)

        return updated_need

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.delete("/{need_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_need(
    need_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NeedService(db)
    need = service.get_by_id(need_id)
    
    if not need:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Need not found",
        )

    ngo = (
        db.query(NGO)
        .filter(NGO.id == need.ngo_id)
        .first()
    )

    if not ngo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NGO not found.",
        )

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != ngo.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this need.",
        )

    try:
        service.delete(need)
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
