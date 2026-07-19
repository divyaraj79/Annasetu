from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.food_category import FoodCategory
from app.enums.quantity_unit import QuantityUnit
from app.enums.status import DonationStatus


class DonationCreate(BaseModel):
    restaurant_id: UUID
    food_name: str
    food_category: FoodCategory
    is_vegetarian: bool
    quantity: int
    quantity_unit: QuantityUnit
    cooked_at: datetime | None = None
    expiry_time: datetime
    pickup_address: str
    special_notes: str | None = None


class DonationUpdate(BaseModel):
    food_name: str | None = None
    food_category: FoodCategory | None = None
    is_vegetarian: bool | None = None
    quantity: int | None = None
    quantity_unit: QuantityUnit | None = None
    cooked_at: datetime | None = None
    expiry_time: datetime | None = None
    pickup_address: str | None = None
    special_notes: str | None = None


class DonationResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    food_name: str
    food_category: FoodCategory
    is_vegetarian: bool
    quantity: int
    quantity_unit: QuantityUnit
    cooked_at: datetime | None = None
    expiry_time: datetime
    pickup_address: str
    latitude: float | None = None
    longitude: float | None = None
    special_notes: str | None = None
    status: DonationStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
