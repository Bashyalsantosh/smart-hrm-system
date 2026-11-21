import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    LAB_TECH = "lab_tech"
    PHARMACIST = "pharmacist"
    RECEPTIONIST = "receptionist"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id"),
        nullable=False
    )

    username = Column(String(100), unique=True, nullable=False, index=True)

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(200), nullable=False)

    role = Column(
        Enum(UserRole),
        nullable=False
    )

    is_active = Column(Boolean, default=True)