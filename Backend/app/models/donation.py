import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.enums.quantity_unit import QuantityUnit
from app.enums.food_category import FoodCategory
from app.enums.status import DonationStatus


class Donation(Base):
    __tablename__ = "donations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        nullable=False
    )

    food_name = Column(String, nullable=False)

    food_category = Column(
        Enum(FoodCategory),
        nullable=False
    )

    is_vegetarian = Column(
        Boolean,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    quantity_unit = Column(
        Enum(QuantityUnit),
        nullable=False
    )

    cooked_at = Column(DateTime)

    expiry_time = Column(
        DateTime,
        nullable=False
    )

    pickup_address = Column(
        String,
        nullable=False
    )

    latitude = Column(Float)

    longitude = Column(Float)

    special_notes = Column(String)

    status = Column(
        Enum(DonationStatus),
        default=DonationStatus.CREATED
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    is_available = Column(
        Boolean,
        default=True,
        nullable=False
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="donations"
    )

    matches = relationship(
        "Match",
        back_populates="donation"
    )