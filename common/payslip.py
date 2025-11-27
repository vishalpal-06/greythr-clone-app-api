# common/payslip.py
from sqlalchemy.orm import Session
from database.models import Payslip
from schema.payslip_schema import PayslipCreate
from fastapi import HTTPException, status
from typing import List
from datetime import datetime
from sqlalchemy import extract


def _get_payslip_or_404(db: Session, payslip_id: int) -> Payslip:
    payslip = db.query(Payslip).filter(Payslip.payslip_id == payslip_id).first()
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
    return payslip


def create_payslip(db: Session, payslip_in: PayslipCreate) -> Payslip:
    # Prevent duplicate payslip for same employee + month
    exists = db.query(Payslip).filter(
        Payslip.fk_employee_id == payslip_in.fk_employee_id,
        Payslip.payslip_month == payslip_in.payslip_month
    ).first()
    if exists:
        raise HTTPException(
            status_code=409,
            detail=f"Payslip already exists for employee {payslip_in.fk_employee_id} in {payslip_in.payslip_month.strftime('%B %Y')}"
        )

    db_payslip = Payslip(**payslip_in.model_dump())
    db.add(db_payslip)
    db.commit()
    db.refresh(db_payslip)
    return db_payslip


def get_payslips_by_employee(db: Session, employee_id: int) -> List[Payslip]:
    payslips = db.query(Payslip)\
        .filter(Payslip.fk_employee_id == employee_id)\
        .order_by(Payslip.payslip_month.desc())\
        .all()
    if not payslips:
        raise HTTPException(status_code=404, detail="No payslips found for this employee")
    return payslips


def get_payslips_by_month(db: Session, year: int, month: int) -> List[Payslip]:
    payslips = db.query(Payslip).filter(
        extract('year', Payslip.payslip_month) == year,
        extract('month', Payslip.payslip_month) == month
    ).all()
    if not payslips:
        raise HTTPException(status_code=404, detail=f"No payslips found for {year}-{month:02d}")
    return payslips


def get_payslip_by_employee_and_month(db: Session, employee_id: int, year: int, month: int) -> Payslip:
    payslip = db.query(Payslip).filter(
        Payslip.fk_employee_id == employee_id,
        extract('year', Payslip.payslip_month) == year,
        extract('month', Payslip.payslip_month) == month
    ).first()
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found for this month")
    return payslip


def delete_payslip_by_id(db: Session, payslip_id: int) -> None:
    payslip = _get_payslip_or_404(db, payslip_id)
    db.delete(payslip)
    db.commit()


def delete_payslip_by_employee_and_month(db: Session, employee_id: int, year: int, month: int) -> None:
    payslip = get_payslip_by_employee_and_month(db, employee_id, year, month)
    db.delete(payslip)
    db.commit()