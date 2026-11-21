from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models import Employee, Organization, User, UserRole


@pytest.fixture()
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with testing_session() as db:
        org = Organization(name="Test Org")
        db.add(org)
        db.flush()
        employee = Employee(
            organization_id=org.id,
            employee_code="EMP-001",
            first_name="Test",
            last_name="Employee",
            email="test.employee@example.com",
            date_joined=date(2025, 1, 1),
        )
        db.add(employee)
        db.flush()
        db.add(User(
            organization_id=org.id,
            employee_id=employee.id,
            username="testuser",
            email="testuser@example.com",
            password_hash=hash_password("correct-horse-battery"),
            role=UserRole.HR_ADMIN,
        ))
        db.commit()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
