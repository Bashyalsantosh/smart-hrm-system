from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models import Employee, User
from app.schemas import EmployeeCreate, EmployeeRead

router = APIRouter(prefix="/api/v1/employees", tags=["employees"])


@router.get("", response_model=list[EmployeeRead])
def list_employees(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return db.query(Employee).filter(
        Employee.organization_id == current_user.organization_id
    ).order_by(Employee.id).limit(200).all()


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("super_admin", "hr_admin")),
):
    employee = Employee(**data.model_dump(), organization_id=current_user.organization_id)
    db.add(employee)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Employee code already exists") from None
    db.refresh(employee)
    return employee


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(
    employee_id: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.organization_id == current_user.organization_id,
    ).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
