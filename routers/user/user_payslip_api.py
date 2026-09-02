# api/user_payslip_api.py

from fastapi import APIRouter

from common.payslip import get_payslip_by_employee_and_month, get_payslips_by_employee
from routers.auth import db_dependency, user_dependency
from schema.payslip_schema import PayslipResponse

router = APIRouter(prefix="/my/payslips", tags=["My - Payslips"])


@router.get("/", response_model=list[PayslipResponse])
def get_my_all_payslips(db: db_dependency, user: user_dependency):
    return get_payslips_by_employee(db=db, employee_id=user["id"])


@router.get("/month/{year}/{month}", response_model=PayslipResponse)
def get_my_payslips_by_month(year: int, month: int, db: db_dependency, user: user_dependency):
    return get_payslip_by_employee_and_month(db=db, employee_id=user["id"], year=year, month=month)
