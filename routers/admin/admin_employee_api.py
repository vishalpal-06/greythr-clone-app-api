from schema.employee_schema import EmployeeResponse, EmployeeCreate, EmployeeUpdate
from typing import List
from routers.auth import db_dependency, user_dependency
from fastapi import APIRouter, status
from common.employee import (
    get_all_employees_common,
    get_employee_by_email_common,
    get_employee_by_id_common,
    create_employee_common,
    update_employee_using_id_common,
    update_employee_using_email_common,
    delete_employee_using_id_common,
    delete_employee_using_email_common
)


router = APIRouter(
    prefix='/admin',
    tags=['Admin => Employee']
)



@router.get("/all_employee/", response_model=List[EmployeeResponse])
def get_all_employees(db: db_dependency, user : user_dependency):
    return get_all_employees_common(db=db,user=user)



@router.get("/get_employee_by_id/", response_model=EmployeeResponse)
def get_employee_by_id(employee_id:int ,db: db_dependency, user : user_dependency):
    return get_employee_by_id_common(employee_id=employee_id, db=db, user=user)



@router.get("/get_employee_by_email/", response_model=EmployeeResponse)
def get_employee_by_email(email:str, db: db_dependency, user : user_dependency):
    return get_employee_by_email_common(employee_email=email, db=db, user=user)



# Create Employee
@router.post("/create_employee/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: db_dependency, user : user_dependency):
    return create_employee_common(employee=employee, db=db, user=user)
    


@router.put("/update_employee_by_id/{employee_id}", response_model=EmployeeResponse)
def update_employee_using_id(employee_id: int, updated_employee_date: EmployeeUpdate, db: db_dependency, user: user_dependency):
    update_employee_using_id_common(
        employee_id=employee_id,
        updated_employee_date=updated_employee_date,
        db=db,
        user=user
    )



@router.put("/update_employee_by_email/{employee_email}", response_model=EmployeeResponse)
def update_employee_using_email(employee_email: str, updated_employee_date: EmployeeUpdate, db: db_dependency, user: user_dependency):
    update_employee_using_email_common(
        employee_email=employee_email,
        updated_employee_date=updated_employee_date,
        db=db,
        user=user
    )


# Delete Employee
@router.delete("/delete_employee_by_id/{employee_id}")
def delete_employee_using_id(employee_id: int, db: db_dependency, user : user_dependency):
    delete_employee_using_id_common(employee_id=employee_id, db=db, user=user)


@router.delete("/delete_employee_by_email/{employee_email}")
def delete_employee_using_email(employee_email: str, db: db_dependency, user : user_dependency):
    delete_employee_using_email_common(employee_email=employee_email, db=db, user=user)