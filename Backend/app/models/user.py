from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.enums.roles import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    phone = Column(String, nullable=False, unique=True, index=True)

    password_hash = Column(String, nullable=True)

    role = Column(Enum(UserRole), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    restaurant = relationship("Restaurant", back_populates="user", uselist=False)

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    ngo = relationship(
        "NGO",
        back_populates="user",
        uselist=False
    )