from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.need import NeedCreate, NeedResponse, NeedUpdate
from app.services.need_service import NeedService

router = APIRouter(prefix="/needs", tags=["needs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=NeedResponse, status_code=status.HTTP_201_CREATED)
def create_need(need: NeedCreate, db: Session = Depends(get_db)):
    service = NeedService(db)

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
def update_need(need_id: UUID, need_data: NeedUpdate, db: Session = Depends(get_db)):
    service = NeedService(db)
    need = service.get_by_id(need_id)
    if not need:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Need not found")
    
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
def delete_need(need_id: UUID, db: Session = Depends(get_db)):
    service = NeedService(db)
    need = service.get_by_id(need_id)
    if not need:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Need not found")
    
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
