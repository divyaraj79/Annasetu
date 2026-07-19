import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, Boolean, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

# from Backend.app.enums.verification_status import VerificationStatus
from app.database import Base
from app.enums.verification_status import VerificationStatus


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_id = Column( UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    restaurant_name = Column(String, nullable=False)

    verification_status = Column(
        Enum(VerificationStatus),
        default=VerificationStatus.PENDING,
        nullable=False
    )

    address = Column(String, nullable=False)

    latitude = Column(Float)

    longitude = Column(Float)

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    user = relationship("User", back_populates="restaurant")

    donations = relationship(
        "Donation",
        back_populates="restaurant"
    )