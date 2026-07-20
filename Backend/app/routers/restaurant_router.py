from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.services.restaurant_service import RestaurantService


from app.auth.dependencies import (
    get_current_user,
    require_role,
)

from app.enums.roles import UserRole
from app.models.user import User

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant: RestaurantCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    )
    ):
    service = RestaurantService(db)
    
    try:
        restaurant = service.create(restaurant)

        db.commit()

        db.refresh(restaurant)

        return restaurant

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: UUID, db: Session = Depends(get_db)):
    service = RestaurantService(db)
    restaurant = service.get_by_id(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return restaurant


@router.get("/", response_model=list[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    service = RestaurantService(db)
    return service.get_all()



@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
        restaurant_id: UUID,
        restaurant_data: RestaurantUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        service = RestaurantService(db)

        restaurant = service.get_by_id(restaurant_id)

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        if (
            current_user.role != UserRole.ADMIN
            and current_user.id != restaurant.user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this restaurant.",
            )

        try:
            updated_restaurant = service.update(
                restaurant,
                restaurant_data,
            )

            db.commit()

            db.refresh(updated_restaurant)

            return updated_restaurant

        except ValueError as e:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        except Exception:
            db.rollback()
            raise


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RestaurantService(db)
    restaurant = service.get_by_id(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != restaurant.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this restaurant.",
        )

    try:
        service.delete(restaurant)

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
