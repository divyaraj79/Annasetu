import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.enums.status import MatchStatus


class Match(Base):
    __tablename__ = "matches"

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

    status = Column(
        Enum(MatchStatus),
        default=MatchStatus.PENDING
    )

    attempt_number = Column(
        Integer,
        nullable=False
    )
    
    matched_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    responded_at = Column(DateTime)

    match_reason = Column(String)

    donation = relationship(
        "Donation",
        back_populates="matches"
    )

    ngo = relationship(
        "NGO",
        back_populates="matches"
    )
