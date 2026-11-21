from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import Attendance, User
from app.schemas import AttendanceRead

router = APIRouter(prefix="/api/v1/attendance", tags=["attendance"])


@router.post("/check-in", response_model=AttendanceRead)
def check_in(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.employee_id is None:
        raise HTTPException(status_code=409, detail="User is not linked to an employee record")
    now = datetime.now(UTC)
    today = now.date()
    record = db.query(Attendance).filter(
        Attendance.organization_id == current_user.organization_id,
        Attendance.employee_id == current_user.employee_id,
        Attendance.attendance_date == today,
    ).first()
    if record and record.check_in is not None:
        raise HTTPException(status_code=409, detail="Already checked in")
    if record is None:
        record = Attendance(
            organization_id=current_user.organization_id,
            employee_id=current_user.employee_id,
            attendance_date=today, check_in=now, status="present",
        )
        db.add(record)
    else:
        record.check_in = now
        record.status = "present"
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Attendance record already exists") from None
    db.refresh(record)
    return record
