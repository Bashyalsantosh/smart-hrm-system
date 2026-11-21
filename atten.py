from sqlalchemy import (
    Column,
    Integer,
    Date,
    DateTime,
    String,
    ForeignKey,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True
    )

    attendance_date = Column(
        Date,
        nullable=False,
        index=True
    )

    check_in = Column(
        DateTime,
        nullable=True
    )

    check_out = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String(20),
        default="present",
        nullable=False
    )

    remarks = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=DateTime
    )

    employee = relationship(
        "Employee"
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "attendance_date",
            name="uq_employee_attendance_date"
        ),
    )