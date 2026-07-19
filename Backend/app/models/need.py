import uuid

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.enums.food_category import FoodCategory
from app.enums.quantity_unit import QuantityUnit
from app.enums.urgency import Urgency
from app.enums.status import DonationStatus


class Need(Base):
    __tablename__ = "needs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    ngo_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ngos.id"),
        nullable=False
    )

    preferred_category = Column(
        Enum(FoodCategory),
        nullable=False
    )

    vegetarian_only = Column(
        Boolean,
        default=False,
        nullable=False
    )

    quantity_required = Column(
        Integer,
        nullable=False
    )

    quantity_unit = Column(
        Enum(QuantityUnit),
        nullable=False
    )

    urgency = Column(
        Enum(Urgency),
        default=Urgency.MEDIUM,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    status = Column(
        Enum(DonationStatus),
        default=DonationStatus.CREATED,
        nullable=False
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    ngo = relationship(
        "NGO",
        back_populates="needs"
    )