from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.quantity_unit import QuantityUnit


class DonationItemCreate(BaseModel):
    donation_id: UUID
    food_name: str
    quantity: int
    quantity_unit: QuantityUnit


class DonationItemUpdate(BaseModel):
    food_name: str | None = None
    quantity: int | None = None
    quantity_unit: QuantityUnit | None = None


class DonationItemResponse(BaseModel):
    id: UUID
    donation_id: UUID
    food_name: str
    quantity: int
    quantity_unit: QuantityUnit
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
