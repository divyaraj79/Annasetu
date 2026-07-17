import uuid

from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class NGO(Base):
    __tablename__ = "ngos"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    ngo_name = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    address = Column(String, nullable=False)

    latitude = Column(Float)

    longitude = Column(Float)

    verified = Column(Boolean, default=False)

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    user = relationship("User", back_populates="ngo")

    needs = relationship(
        "Need",
        back_populates="ngo"
    )

    matches = relationship(
        "Match",
        back_populates="ngo"
    )