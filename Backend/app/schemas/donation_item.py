from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)

from app.enums.quantity_unit import QuantityUnit


class DonationItemCreate(BaseModel):
    donation_id: UUID
    food_name: str
    quantity: int
    quantity_unit: QuantityUnit

    @field_validator("food_name")
    @classmethod
    def validate_food_name(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Food name must contain at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Food name cannot exceed 100 characters."
            )

        return value


class DonationItemUpdate(BaseModel):
    food_name: str | None = None
    quantity: int | None = None
    quantity_unit: QuantityUnit | None = None

    @field_validator("food_name")
    @classmethod
    def validate_food_name(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Food name must contain at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Food name cannot exceed 100 characters."
            )

        return value


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
