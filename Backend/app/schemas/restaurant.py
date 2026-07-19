from uuid import UUID

from pydantic import BaseModel, ConfigDict
from app.enums.verification_status import VerificationStatus


class RestaurantCreate(BaseModel):
    user_id: UUID
    restaurant_name: str
    address: str


class RestaurantUpdate(BaseModel):
    restaurant_name: str | None = None
    address: str | None = None

class RestaurantResponse(BaseModel):
    id: UUID
    user_id: UUID
    restaurant_name: str
    verification_status: VerificationStatus
    address: str
    latitude: float | None = None
    longitude: float | None = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
