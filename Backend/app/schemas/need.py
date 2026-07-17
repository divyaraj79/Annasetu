from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.food_category import FoodCategory
from app.enums.quantity_unit import QuantityUnit
from app.enums.urgency import Urgency


class NeedCreate(BaseModel):
    ngo_id: UUID
    preferred_category: FoodCategory
    vegetarian_only: bool = False
    quantity_required: int
    quantity_unit: QuantityUnit
    urgency: Urgency = Urgency.MEDIUM


class NeedUpdate(BaseModel):
    ngo_id: UUID | None = None
    preferred_category: FoodCategory | None = None
    vegetarian_only: bool | None = None
    quantity_required: int | None = None
    quantity_unit: QuantityUnit | None = None
    urgency: Urgency | None = None
    is_deleted: bool | None = None


class NeedResponse(BaseModel):
    id: UUID
    ngo_id: UUID
    preferred_category: FoodCategory
    vegetarian_only: bool
    quantity_required: int
    quantity_unit: QuantityUnit
    urgency: Urgency
    updated_at: datetime | None = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
