from datetime import date
from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    middle_name: str | None = None
    last_name: str = Field(min_length=2, max_length=100)

    first_name_ne: str | None = None
    last_name_ne: str | None = None

    date_of_birth: date | None = None

    gender: str | None = None
    blood_group: str | None = None

    phone: str = Field(min_length=7, max_length=30)

    email: str | None = None
    address: str | None = None

    municipality: str | None = None
    district: str | None = None
    province: str | None = None

    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None


class PatientResponse(BaseModel):
    id: int
    uhid: str
    first_name: str
    last_name: str
    phone: str
    status: str

    class Config:
        from_attributes = True