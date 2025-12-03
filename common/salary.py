# common/salary.py
from sqlalchemy.orm import Session
from database.models import Salary
from schema.salary_schema import SalaryCreate
from typing import List
from fastapi import HTTPException, status


# ─── READ OPERATIONS (with proper exceptions) ────────────────────────────────
def get_salaries_by_year(db: Session, year: int) -> List[Salary]:
    salaries = db.query(Salary).filter(Salary.salary_year == year).all()
    if not salaries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No salary records found for year {year}"
        )
    return salaries


def get_salary_by_employee_and_year(db: Session, employee_id: int, year: int) -> Salary:
    salary = (
        db.query(Salary)
        .filter(Salary.fk_employee_id == employee_id, Salary.salary_year == year)
        .first()
    )
    if not salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salary record not found for employee in year {year}"
        )
    return salary


def get_salaries_by_employee_id(db: Session, employee_id: int) -> List[Salary]:
    salaries = db.query(Salary).filter(Salary.fk_employee_id == employee_id).all()
    if not salaries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No salary records found for employee {employee_id}"
        )
    return salaries


# ─── CREATE (with duplicate check) ───────────────────────────────────────────
def create_salary(db: Session, salary: SalaryCreate) -> Salary:
    # Check for duplicate: same employee + same year
    exists = (
        db.query(Salary)
        .filter(
            Salary.fk_employee_id == salary.fk_employee_id,
            Salary.salary_year == salary.salary_year
        )
        .first()
    )
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Salary record already exists for employee {salary.fk_employee_id} in year {salary.salary_year}"
        )

    db_salary = Salary(**salary.model_dump())
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


# ─── DELETE ──────────────────────────────────────────────────────────────────
def delete_salary(db: Session, salary_id: int) -> None:
    db_salary = db.query(Salary).filter(Salary.salary_id == salary_id).first()
    if not db_salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salary record with ID {salary_id} not found"
        )
    db.delete(db_salary)
    db.commit()


def delete_salary_by_employee_and_year(db: Session, employee_id: int, year: int) -> None:
    """
    Deletes salary record for a specific employee in a specific year.
    Raises HTTPException if not found.
    """
    salary = get_salary_by_employee_and_year(db, employee_id, year)
    
    db.delete(salary)
    db.commit()