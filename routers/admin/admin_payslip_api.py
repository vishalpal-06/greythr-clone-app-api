# api/admin_payslip_api.py
from fastapi import APIRouter, status
from typing import List
from schema.payslip_schema import PayslipCreate, PayslipResponse
from routers.auth import db_dependency, user_dependency
from common.common import _require_admin
from common.payslip import (
    create_payslip,
    get_payslips_by_employee,
    get_payslips_by_month,
    get_payslip_by_employee_and_month,
    delete_payslip_by_id,
    delete_payslip_by_employee_and_month,
)

router = APIRouter(prefix="/admin/payslips", tags=["Admin - Payslip"])


@router.post("/", response_model=PayslipResponse, status_code=status.HTTP_201_CREATED)
def create_payslips(payslip_in: PayslipCreate, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return create_payslip(db=db, payslip_in=payslip_in)


@router.get("/employee/{employee_id}", response_model=List[PayslipResponse])
def get_payslips_by_employeeid(employee_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_payslips_by_employee(db=db, employee_id=employee_id)


@router.get("/month/{year}/{month}", response_model=List[PayslipResponse])
def get_payslips_by_month_endpoint(year: int, month: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    return get_payslips_by_month(db=db, year=year, month=month)


@router.get("/employee/{employee_id}/month/{year}/{month}", response_model=PayslipResponse)
def get_payslips_by_month_and_employeeid(
    employee_id: int, year: int, month: int, db: db_dependency, user: user_dependency
):
    _require_admin(user)
    return get_payslip_by_employee_and_month(db=db, employee_id=employee_id, year=year, month=month)


@router.delete("/{payslip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payslips_by_id(payslip_id: int, db: db_dependency, user: user_dependency):
    _require_admin(user)
    delete_payslip_by_id(db=db, payslip_id=payslip_id)


@router.delete("/employee/{employee_id}/month/{year}/{month}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_employeeid_and_month(
    employee_id: int, year: int, month: int, db: db_dependency, user: user_dependency
):
    _require_admin(user)
    delete_payslip_by_employee_and_month(db=db, employee_id=employee_id, year=year, month=month)