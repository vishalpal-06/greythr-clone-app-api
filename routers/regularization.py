from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Enum
from database.models import Regularization, Employee, Status
from routers.auth import user_dependency, db_dependency
from pydantic import BaseModel
from datetime import date
from sqlalchemy import Date, cast, func


router = APIRouter(prefix="/regularization", tags=["Regularization"])

class RegularizationBase(BaseModel):
    date: date
    reason: str


class RegularizationResponse(RegularizationBase):
    regularization_id:int
    manager_id:int
    employee_id: int
    status: str


class RegularizationCreate(RegularizationBase):
    pass
    
class RegularizationUpdate(BaseModel):
    status: Status



#Create Regularization
@router.post("/create_regularization")
async def create_regularization(regularization_form: RegularizationCreate, db: db_dependency, user : user_dependency):

    regularization = db.query(Regularization).filter(
        Regularization.fk_employee_id == user['id']).filter(
        func.date(Regularization.regularization_date) == regularization_form.date
    ).first()
    if regularization:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Regularization for date {regularization_form.date} has already been applied")
    
    user_details = db.query(Employee).filter(Employee.employee_id == user['id']).first()

    new_regularization = Regularization(
        regularization_date = regularization_form.date,
        regularization_reason = regularization_form.reason,
        fk_employee_id = user_details.employee_id,
        fk_manager_id = user_details.fk_manager_id
    )
    db.add(new_regularization)
    db.commit()
    db.refresh(new_regularization)
    return new_regularization



@router.get("/get_regularization_by_date")
async def get_regularization_by_date(regularization_date: date, db: db_dependency, user : user_dependency):
    
    regularization_record = (
        db.query(Regularization)
        .filter(func.date(Regularization.regularization_date) == regularization_date, Regularization.fk_employee_id == user['id'])
        .all()
    )
    return regularization_record



@router.get("/get_all_regularization")
async def get_all_regularization(db: db_dependency, user : user_dependency):
    regularization_record = (
        db.query(Regularization)
        .filter(Regularization.fk_employee_id == user['id'])
        .all()
    )
    return regularization_record



#Update Regularization
@router.put("/update_regularization_status/{regularization_id}")
async def update_regularization_status(regularization_id: int, regularization_form: RegularizationUpdate, db: db_dependency, user : user_dependency):
    regularization_record = db.query(Regularization).filter(Regularization.regularization_id == regularization_id).first()
    if not regularization_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Regularization record not found")
    if regularization_record.fk_manager_id == user['id']:
        regularization_record.regularization_status = regularization_form.status
        db.commit()
        db.refresh(regularization_record)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return {"message": "Regularization status updated successfully", "data": regularization_record}



#Delete Regularization
@router.delete("/delete_regularization")
async def delete_regularization(regularization_id: int, db: db_dependency, user : user_dependency):
    regularization = db.query(Regularization).filter(Regularization.regularization_id == regularization_id).first()
    if not regularization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Regularization record not found")
    if regularization.fk_employee_id == user['id']:
        db.delete(regularization)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return {"message": "Regularization deleted successfully"}