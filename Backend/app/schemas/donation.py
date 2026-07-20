from datetime import datetime, timezone
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)

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
    
    @field_validator("cooked_at", "expiry_time")
    @classmethod
    def validate_timezone(
        cls,
        value: datetime | None,
    ) -> datetime | None:

        if value is None:
            return value

        if (
            value.tzinfo is None
            or value.tzinfo.utcoffset(value) is None
        ):
            raise ValueError(
                "Datetime must include timezone information."
            )

        return value
    
    @field_validator("pickup_address")
    @classmethod
    def validate_pickup_address(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if len(value) < 5:
            raise ValueError(
                "Pickup address must contain at least 5 characters."
            )

        if len(value) > 300:
            raise ValueError(
                "Pickup address cannot exceed 300 characters."
            )

        return value
    
    @field_validator("special_notes")
    @classmethod
    def validate_special_notes(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if len(value) > 500:
            raise ValueError(
                "Special notes cannot exceed 500 characters."
            )

        return value


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
    
    @field_validator("cooked_at", "expiry_time")
    @classmethod
    def validate_timezone(
        cls,
        value: datetime | None,
    ) -> datetime | None:

        if value is None:
            return value

        if (
            value.tzinfo is None
            or value.tzinfo.utcoffset(value) is None
        ):
            raise ValueError(
                "Datetime must include timezone information."
            )

        return value
    
    @field_validator("pickup_address")
    @classmethod
    def validate_pickup_address(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if len(value) < 5:
            raise ValueError(
                "Pickup address must contain at least 5 characters."
            )

        if len(value) > 300:
            raise ValueError(
                "Pickup address cannot exceed 300 characters."
            )

        return value
    
    @field_validator("special_notes")
    @classmethod
    def validate_special_notes(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if len(value) > 500:
            raise ValueError(
                "Special notes cannot exceed 500 characters."
            )

        return value




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
