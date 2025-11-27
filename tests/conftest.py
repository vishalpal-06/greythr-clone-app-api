import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database.models import Base, Department, Role, Employee
from datetime import date
from routers.auth import get_db


# ------------------------------
# TEST DATABASE SETUP
# ------------------------------
TEST_DB_URL = "sqlite:///./test_db.sqlite3"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ------------------------------
# DATABASE FIXTURE
# ------------------------------
@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    # Seed departments
    session.add_all([
        Department(department_name="Human Resources"),
        Department(department_name="Finance"),
        Department(department_name="Engineering"),
        Department(department_name="Sales"),
    ])
    session.commit()

    # Seed roles
    session.add_all([
        Role(role="Manager"),
        Role(role="Developer"),
        Role(role="Accountant"),
        Role(role="HR Executive")
    ])
    session.commit()

    # Seed employees
    session.add_all([
        Employee(
            first_name="admin",
            last_name="Pal",
            email="admin@test.com",
            password="pass123",
            joining_date=date(2023, 5, 18),
            address="Kalyan",
            fk_department_id=1,
            fk_role_id=1,
            isadmin=1
        ),
        Employee(
            first_name="manager",
            last_name="Pal",
            email="manager@test.com",
            password="pass123",
            joining_date=date(2023, 1, 15),
            address="NY",
            fk_department_id=2,
            fk_role_id=2,
            isadmin=0
        ),
        Employee(
            first_name="juniour",
            last_name="Pal",
            email="juniour@test.com",
            password="pass123",
            joining_date=date(2023, 1, 15),
            address="NY",
            fk_department_id=2,
            fk_role_id=2,
            isadmin=0,
            fk_manager_id=2
        )
    ])
    session.commit()

    try:
        yield session
    finally:
        session.close()


# ------------------------------
# OVERRIDE get_db DEPENDENCY
# ------------------------------
@pytest.fixture
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


# ------------------------------
# AUTH HELPER FUNCTION
# ------------------------------
def get_auth_token(client, email: str, password: str) -> str:
    """Generate JWT token using /auth/token."""
    response = client.post(
        "/auth/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200, "Failed to get token"
    return response.json()["access_token"]


# ------------------------------
# TOKEN FIXTURE (optional)
# ------------------------------
@pytest.fixture
def admin_token(client):
    return get_auth_token(client, "admin@test.com", "pass123")


@pytest.fixture
def user_token(client):
    return get_auth_token(client, "juniour@test.com", "pass123")

@pytest.fixture
def manager_token(client):
    return get_auth_token(client, "manager@test.com", "pass123")