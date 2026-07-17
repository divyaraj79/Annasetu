from uuid import UUID

from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, restaurant_data: RestaurantCreate) -> Restaurant:
        restaurant = Restaurant(**restaurant_data.model_dump())
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def get_by_id(self, restaurant_id: UUID) -> Restaurant | None:
        return self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def get_all(self) -> list[Restaurant]:
        return self.db.query(Restaurant).all()

    def update(self, restaurant: Restaurant, restaurant_data: RestaurantUpdate) -> Restaurant:
        for field, value in restaurant_data.model_dump(exclude_unset=True).items():
            setattr(restaurant, field, value)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def delete(self, restaurant: Restaurant) -> None:
        self.db.delete(restaurant)
        self.db.commit()
