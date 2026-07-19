import uuid

from sqlalchemy import (
    Column,
    String,
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
from app.enums.quantity_unit import QuantityUnit


class DonationItem(Base):
    __tablename__ = "donation_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    donation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("donations.id"),
        nullable=False
    )

    food_name = Column(String, nullable=False)

    quantity = Column(
        Integer,
        nullable=False
    )

    quantity_unit = Column(
        Enum(QuantityUnit),
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

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    donation = relationship(
        "Donation",
        back_populates="donation_items"
    )
