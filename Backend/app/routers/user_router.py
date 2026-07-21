from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

from app.auth.dependencies import (
    get_current_user,
    require_role,
)

from app.enums.roles import UserRole
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


# I am tuning it of as there should be only one way to create user and that is registration service
# @router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def create_user(
#     user: UserCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_role(UserRole.ADMIN)
#     ),
# ):
#     service = UserService(db)

#     try:
#         created_user = service.create(user)

#         db.commit()

#         db.refresh(created_user)

#         return created_user

#     except ValueError as e:
#         db.rollback()

#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )

#     except Exception:
#         db.rollback()
#         raise


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):    
    service = UserService(db)
    user = service.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this user.",
        )

    return user


@router.get("/", response_model=list[UserResponse] )
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    )  
    ):
    service = UserService(db)
    return service.get_all()


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    user = service.get_by_id(user_id)

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user.",
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    try:
        updated_user = service.update(user, user_data)

        db.commit()

        db.refresh(updated_user)

        return updated_user

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserService(db)
    user = service.get_by_id(user_id)

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this user.",
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    try:
        service.delete(user)

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
