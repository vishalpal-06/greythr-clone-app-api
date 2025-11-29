import sys, os
# Remove unused imports (e.g., json, datetime, date, all models except Base)
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .seed_db import seed_all_tables

from main import app
from database.models import Base 
from routers.auth import get_db

# ... (rest of the initial setup and imports remain the same)

# ------------------------------
# TEST DATABASE SETUP
# ------------------------------
TEST_DB_URL = "sqlite:///./test_db.sqlite3"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Determine the base directory for test data once
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

# REMOVE load_json_data function from here, it's now in seed_db.py

# ------------------------------
# DATABASE FIXTURE
# ------------------------------
@pytest.fixture
def db_session():
    # 1. Setup DB Schema
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    
    # 2. Seed Data using the new external function
    # Pass the session and the path to the test data directory
    seed_all_tables(session, TEST_DATA_DIR) 

    # 3. Yield the session for tests and clean up
    try:
        yield session
    finally:
        session.close()

# ... (rest of conftest.py remains the same, including client, tokens, etc.)


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
def manager_A(client):
    return get_auth_token(client, "managerA@test.com", "pass123")


@pytest.fixture
def manager_B(client):
    return get_auth_token(client, "managerB@test.com", "pass123")


@pytest.fixture
def user_A1(client):
    return get_auth_token(client, "userA1@test.com", "pass123")


@pytest.fixture
def user_A2(client):
    return get_auth_token(client, "userA2@test.com", "pass123")


@pytest.fixture
def user_B1(client):
    return get_auth_token(client, "userB1@test.com", "pass123")


@pytest.fixture
def user_B2(client):
    return get_auth_token(client, "userB2@test.com", "pass123")
