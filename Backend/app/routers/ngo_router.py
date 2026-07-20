from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ngo import NGOCreate, NGOResponse, NGOUpdate
from app.services.ngo_service import NGOService

from app.auth.dependencies import (
    get_current_user,
    require_role,
)

from app.enums.roles import UserRole
from app.models.user import User

router = APIRouter(prefix="/ngos", tags=["ngos"])

@router.post("/", response_model=NGOResponse, status_code=status.HTTP_201_CREATED)
def create_ngo(
    ngo: NGOCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    )
    ):
    service = NGOService(db)

    try:
        created_ngo = service.create(ngo)

        db.commit()

        db.refresh(created_ngo)

        return created_ngo

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.get("/{ngo_id}", response_model=NGOResponse)
def get_ngo(ngo_id: UUID, db: Session = Depends(get_db)):
    service = NGOService(db)
    ngo = service.get_by_id(ngo_id)
    if not ngo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NGO not found")
    return ngo


@router.get("/", response_model=list[NGOResponse])
def get_ngos(db: Session = Depends(get_db)):
    service = NGOService(db)
    return service.get_all()


@router.put("/{ngo_id}", response_model=NGOResponse)
def update_ngo(
    ngo_id: UUID, 
    ngo_data: NGOUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    service = NGOService(db)

    ngo = service.get_by_id(ngo_id)

    if not ngo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NGO not found"
        )
    
    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != ngo.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this NGO.",
        )

    try:
        updated_ngo = service.update(
            ngo,
            ngo_data,
        )

        db.commit()

        db.refresh(updated_ngo)

        return updated_ngo

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 

    except Exception:
        db.rollback()
        raise 


@router.delete("/{ngo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ngo(
    ngo_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    service = NGOService(db)

    ngo = service.get_by_id(ngo_id)

    if not ngo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NGO not found"
        )
    
    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != ngo.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this NGO.",
        )

    try:
        service.delete(ngo)

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
