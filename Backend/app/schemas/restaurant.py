from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)
from app.enums.verification_status import VerificationStatus


class RestaurantCreate(BaseModel):
    user_id: UUID
    restaurant_name: str
    address: str

    @field_validator("restaurant_name")
    @classmethod
    def validate_restaurant_name(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Restaurant name must contain at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Restaurant name cannot exceed 100 characters."
            )

        return value

    @field_validator("address")
    @classmethod
    def validate_address(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if len(value) < 5:
            raise ValueError(
                "Address must contain at least 5 characters."
            )

        if len(value) > 300:
            raise ValueError(
                "Address cannot exceed 300 characters."
            )

        return value


class RestaurantUpdate(BaseModel):
    restaurant_name: str | None = None
    address: str | None = None

    @field_validator("restaurant_name")
    @classmethod
    def validate_restaurant_name(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Restaurant name must contain at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Restaurant name cannot exceed 100 characters."
            )

        return value

    @field_validator("address")
    @classmethod
    def validate_address(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if len(value) < 5:
            raise ValueError(
                "Address must contain at least 5 characters."
            )

        if len(value) > 300:
            raise ValueError(
                "Address cannot exceed 300 characters."
            )

        return value

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
