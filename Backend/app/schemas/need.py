from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.food_category import FoodCategory
from app.enums.quantity_unit import QuantityUnit
from app.enums.urgency import Urgency
from app.enums.status import DonationStatus


class NeedCreate(BaseModel):
    ngo_id: UUID
    preferred_category: FoodCategory
    vegetarian_only: bool = False
    quantity_required: int
    quantity_unit: QuantityUnit
    urgency: Urgency = Urgency.MEDIUM


class NeedUpdate(BaseModel):
    preferred_category: FoodCategory | None = None
    vegetarian_only: bool | None = None
    quantity_required: int | None = None
    quantity_unit: QuantityUnit | None = None
    urgency: Urgency | None = None


class NeedResponse(BaseModel):
    id: UUID
    ngo_id: UUID
    preferred_category: FoodCategory
    vegetarian_only: bool
    quantity_required: int
    quantity_unit: QuantityUnit
    urgency: Urgency
    created_at: datetime | None = None
    updated_at: datetime | None = None
    status: DonationStatus
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
