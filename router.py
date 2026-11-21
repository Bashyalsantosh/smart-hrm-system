@router.post(
    "/check-in/{employee_id}",
    response_model=AttendanceResponse
)
def check_in(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    today = date.today()

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == today
        )
        .first()
    )

    if attendance and attendance.check_in:
        raise HTTPException(
            status_code=400,
            detail="Employee already checked in"
        )

    if not attendance:
        attendance = Attendance(
            employee_id=employee_id,
            attendance_date=today,
            check_in=datetime.now(),
            status="present"
        )

        db.add(attendance)

    else:
        attendance.check_in = datetime.now()
        attendance.status = "present"

    db.commit()
    db.refresh(attendance)

    return attendance