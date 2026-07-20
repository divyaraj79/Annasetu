import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Boolean
)
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.enums.status import MatchStatus


class Match(Base):
    __tablename__ = "matches"

    __table_args__ = (
        UniqueConstraint(
            "donation_id",
            "ngo_id",
            name="uq_match_donation_ngo",
        ),
    )

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

    ngo_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ngos.id"),
        nullable=False
    )

    score = Column(Float)

    distance_km = Column(Float, nullable=False)

    status = Column(
        Enum(MatchStatus),
        default=MatchStatus.PENDING,
        nullable=False
    )

    attempt_number = Column(
        Integer,
        nullable=False
    )
    
    matched_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    responded_at = Column(DateTime(timezone=True))

    match_reason = Column(String)

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    donation = relationship(
        "Donation",
        back_populates="matches"
    )

    ngo = relationship(
        "NGO",
        back_populates="matches"
    )
