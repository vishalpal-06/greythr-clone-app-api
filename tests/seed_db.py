# seed_db.py

import json
import os
import datetime
from datetime import date
import pytest
from sqlalchemy.orm import Session
from database.models import Department, Role, Employee, Attendance, Salary, Leave, LeaveApplication, Regularization, Payslip, ExpenseClaim 

def load_json_data(base_path: str, filename: str):
    """Helper function to load a JSON file from the specified directory."""
    file_path = os.path.join(base_path, filename)
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pytest.fail(f"Seed data file not found: {file_path}")
    except json.JSONDecodeError:
        pytest.fail(f"Error decoding JSON from file: {file_path}")


def seed_all_tables(session: Session, test_data_dir: str):
    """
    Loads all seed data from JSON files and populates the database tables.

    Args:
        session: The SQLAlchemy Session object to commit data to.
        test_data_dir: The path to the directory containing the JSON files.
    """

    # --- Seed Departments ---
    departments_data = load_json_data(test_data_dir, "departments.json")
    session.add_all([Department(department_name=d["department_name"]) for d in departments_data])
    session.commit()

    # --- Seed Roles ---
    roles_data = load_json_data(test_data_dir, "roles.json")
    session.add_all([Role(role=r["role"]) for r in roles_data])
    session.commit()

    # --- Seed Employees ---
    employees_data = load_json_data(test_data_dir, "employees.json")
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

    # --- Seed Attendance ---
    attendance_data = load_json_data(test_data_dir, "attendance.json")
    attendance_to_add = [
        Attendance(
            punch_time=datetime.datetime.fromisoformat(e["punch_time"]),
            fk_employee_id=e['fk_employee_id']
        )
        for e in attendance_data
    ]
    session.add_all(attendance_to_add)
    session.commit()
    
    # ... Continue with all other seeding blocks, replacing `load_json_data("filename")` 
    #     with `load_json_data(test_data_dir, "filename")` 
    #     and ensuring all necessary imports are at the top (datetime, date, models, etc.).

    # --- Seed Salary ---
    salary_data = load_json_data(test_data_dir, "salary.json")
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

    # --- Seed Leaves ---
    leaves_data = load_json_data(test_data_dir, "leaves.json")
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

    # --- Seed Leave Applications ---
    applications_data = load_json_data(test_data_dir, "leave_applications.json")
    applications_to_add = [
        LeaveApplication( 
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
    session.add_all(applications_to_add)
    session.commit()

    # --- Seed Regularizations ---
    regularizations_data = load_json_data(test_data_dir, "regularizations.json")
    regularizations_to_add = [
        Regularization( 
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
    
    # --- Seed Payslips ---
    payslips_data = load_json_data(test_data_dir, "payslips.json")
    payslips_to_add = [
        Payslip(
            basic_amount=e["basic_amount"],
            hra=e["hra"],
            special_allowance=e["special_allowance"],
            internet_allowance=e["internet_allowance"],
            payslip_month=datetime.datetime.fromisoformat(e["payslip_month"]),
            fk_employee_id=e["fk_employee_id"],
        )
        for e in payslips_data
    ]
    session.add_all(payslips_to_add)
    session.commit()

    # --- Seed Expense Claims ---
    expense_claims_data = load_json_data(test_data_dir, "expense_claims.json")
    expense_claims_to_add = [
        ExpenseClaim( 
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