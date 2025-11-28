import sys, os
from datetime import date
import datetime
import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database.models import Base, Department, Role, Employee, Attendance, Salary, Leave, LeaveApplication, Regularization, Payslip, ExpenseClaim
from routers.auth import get_db

UTC = datetime.timezone.utc
# ------------------------------
# TEST DATABASE SETUP
# ------------------------------
TEST_DB_URL = "sqlite:///./test_db.sqlite3"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Determine the base directory for test data once
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

def load_json_data(filename: str):
    """Helper function to load a JSON file from the test_data directory."""
    file_path = os.path.join(TEST_DATA_DIR, filename)
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pytest.fail(f"Seed data file not found: {file_path}")
    except json.JSONDecodeError:
        pytest.fail(f"Error decoding JSON from file: {file_path}")


# ------------------------------
# DATABASE FIXTURE
# ------------------------------
@pytest.fixture
def db_session():
    # 1. Setup DB Schema
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    
    # 2. Seed Data using the helper function
    
    # Seed Departments
    departments_data = load_json_data("departments.json")
    session.add_all([Department(department_name=d["department_name"]) for d in departments_data])
    session.commit()

    # Seed Roles
    roles_data = load_json_data("roles.json")
    session.add_all([Role(role=r["role"]) for r in roles_data])
    session.commit()

    # Seed Employees
    employees_data = load_json_data("employees.json")
    employees_to_add = [
        Employee(
            first_name=e["first_name"],
            last_name=e["last_name"],
            email=e["email"],
            password=e["password"],
            joining_date=date.fromisoformat(e["joining_date"]), 
            address=e["address"],
            fk_department_id=e["fk_department_id"],
            fk_role_id=e["fk_role_id"],
            isadmin=e["isadmin"],
            fk_manager_id=e["fk_manager_id"],
        )
        for e in employees_data
    ]
    session.add_all(employees_to_add)
    session.commit()

    # Seed Attendance
    attendance_data = load_json_data("attendance.json")
    attendance_to_add = [
        Attendance(
            # fromisoformat handles the 'Z' (UTC) suffix correctly by default
            punch_time=datetime.datetime.fromisoformat(e["punch_time"]),
            fk_employee_id=e['fk_employee_id']
        )
        for e in attendance_data
    ]
    session.add_all(attendance_to_add)
    session.commit()

    # Seed Salary
    salary_data = load_json_data("salary.json")
    salary_to_add = [
        Salary(
            salary_year=e["salary_year"],
            lpa=e['lpa'],
            fk_employee_id=e['fk_employee_id']
        )
        for e in salary_data
    ]
    session.add_all(salary_to_add)
    session.commit()

    # Seed Leaves
    leaves_data = load_json_data("leaves.json")
    leaves_to_add = [
        Leave(
            assign_year=e['assign_year'],
            casual_leave= e['casual_leave'],
            plan_leave= e['plan_leave'],
            probation_leave= e['probation_leave'],
            sick_leave= e['sick_leave'],
            total_leave= e['total_leave'],
            balance_leave= e['balance_leave'],
            fk_employee_id= e['fk_employee_id']
        )
        for e in leaves_data
    ]
    session.add_all(leaves_to_add)
    session.commit()

    # Seed Leave Applications
    applications_data = load_json_data("leave_applications.json")
    attendance_to_add = [
        LeaveApplication( # Make sure to import the LeaveApplication class
            from_date=datetime.datetime.fromisoformat(e["from_date"]),
            end_date=datetime.datetime.fromisoformat(e["end_date"]),
            total_days=e["total_days"],
            leave_status=e["leave_status"], 
            leave_reason=e["leave_reason"],
            fk_employee_id=e["fk_employee_id"],
            fk_manager_id=e["fk_manager_id"]
        )
        for e in applications_data
    ]
    session.add_all(attendance_to_add)
    session.commit()

    # Seed Regularizations
    regularizations_data = load_json_data("regularizations.json")
    regularizations_to_add = [
        Regularization( # Make sure to import the Regularization class
            regularization_start_time=datetime.datetime.fromisoformat(e["regularization_start_time"]),
            regularization_end_time=datetime.datetime.fromisoformat(e["regularization_end_time"]),
            regularization_reason=e["regularization_reason"],
            regularization_status=e["regularization_status"],
            fk_employee_id=e["fk_employee_id"],
            fk_manager_id=e["fk_manager_id"],
        )
        for e in regularizations_data
    ]
    session.add_all(regularizations_to_add)
    session.commit()
    
    # Seed Payslips
    payslips_data = load_json_data("payslips.json")
    payslips_to_add = [
        Payslip(
            basic_amount=e["basic_amount"],
            hra=e["hra"],
            special_allowance=e["special_allowance"],
            internet_allowance=e["internet_allowance"],
            # Convert the month string to a datetime object
            payslip_month=datetime.datetime.fromisoformat(e["payslip_month"]),
            fk_employee_id=e["fk_employee_id"],
        )
        for e in payslips_data
    ]
    session.add_all(payslips_to_add)
    session.commit()

    # Seed Expense Claims
    expense_claims_data = load_json_data("expense_claims.json")
    expense_claims_to_add = [
        ExpenseClaim( # Make sure to import the ExpenseClaim class
            claim_date=datetime.datetime.fromisoformat(claim["claim_date"]),
            amount=claim["amount"],
            description=claim["description"],
            claim_status=claim["claim_status"],
            fk_employee_id=claim["fk_employee_id"],
            fk_manager_id=claim["fk_manager_id"],
        )
        for claim in expense_claims_data
    ]
    session.add_all(expense_claims_to_add)
    session.commit()

    # 3. Yield the session for tests and clean up
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
def manager_A(client):
    return get_auth_token(client, "managerA@test.com", "pass123")


@pytest.fixture
def manager_B(client):
    return get_auth_token(client, "managerB@test.com", "pass123")


@pytest.fixture
def user_A1(client):
    return get_auth_token(client, "userA1@test.com", "pass123")


@pytest.fixture
def user_A1(client):
    return get_auth_token(client, "userA2@test.com", "pass123")


@pytest.fixture
def user_A1(client):
    return get_auth_token(client, "userB1@test.com", "pass123")


@pytest.fixture
def user_A1(client):
    return get_auth_token(client, "userB2@test.com", "pass123")
