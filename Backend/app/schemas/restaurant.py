from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RestaurantCreate(BaseModel):
    user_id: UUID
    restaurant_name: str
    phone: str
    address: str
    latitude: float | None = None
    longitude: float | None = None


class RestaurantUpdate(BaseModel):
    user_id: UUID | None = None
    restaurant_name: str | None = None
    phone: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_deleted: bool | None = None


class RestaurantResponse(BaseModel):
    id: UUID
    user_id: UUID
    restaurant_name: str
    phone: str
    address: str
    latitude: float | None = None
    longitude: float | None = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
