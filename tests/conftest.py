import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .seed_db import seed_all_tables
import json
from pathlib import Path
from main import app
from database.models import Base
from routers.auth import get_db
import os
import inspect

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
def admin_user(client):
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


@pytest.fixture
def read_json(request: pytest.FixtureRequest):  # pragma: no cover
    """
    Smart read_json that:
    - Loads expected JSON from file (normal mode)
    - OR saves the current 'response.json()' to the file if UPDATE_TEST_DATA=1

    Usage (no changes needed in your 500+ tests):
        expected = read_json("path/to/expected.json")
    """
    update_mode = os.getenv("UPDATE_TEST_DATA") in ("1", "true", "True", "yes", "YES")

    def _read_json(file_name: str):
        file_path = Path(__file__).parent / file_name

        # Try to find the 'response' object in the calling test
        response_data = None

        # Walk up the call stack to find the test function frame
        frame = inspect.currentframe()
        while frame:
            if "response" in frame.f_locals:
                resp_obj = frame.f_locals["response"]
                if hasattr(resp_obj, "json"):
                    try:
                        response_data = resp_obj.json()
                        break
                    except:
                        pass
            frame = frame.f_back

        # Update mode: save if we found response data
        if update_mode and response_data is not None:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print(f"\nUPDATED test data: {file_path}")
            return response_data

        # Normal mode: just load the file
        if not file_path.exists():
            raise FileNotFoundError(
                f"Expected file not found: {file_path}\n"
                "Run tests with UPDATE_TEST_DATA=1 to generate it automatically."
            )

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    return _read_json
