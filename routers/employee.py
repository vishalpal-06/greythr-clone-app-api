from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from database.models import Employee
from routers.auth import user_dependency,db_dependency

router = APIRouter(
    prefix='/employee',
    tags=['Employee']
)



class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    joining_date: date
    address: Optional[str] = None
    isadmin: bool
    fk_department_id: int
    fk_role_id: int
    fk_manager_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeResponse(EmployeeBase):
    employee_id: int

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    joining_date: Optional[date] = None
    address: Optional[str] = None
    isadmin: Optional[bool] = None
    fk_department_id: Optional[int] = None
    fk_role_id: Optional[int] = None
    fk_manager_id: Optional[int] = None
    password: Optional[str] = None






# Create Employee
@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: db_dependency, user : user_dependency):
    if user['is_admin']:
        existing = db.query(Employee).filter(Employee.email == employee.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee with this email already exist")

        new_employee = Employee(**employee.model_dump())
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return new_employee
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only users with administrator privileges can create new employees.")


# Get All Employees
@router.get("/", response_model=List[EmployeeResponse])
async def get_employees(db: db_dependency, user : user_dependency):
    if user['is_admin']:
        return db.query(Employee).all()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")


# Get Employee by ID
@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, db: db_dependency, user : user_dependency):
    if user['is_admin'] or user['id']==employee_id:
        emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return emp
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")


# Update Employee
@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: int, updated: EmployeeUpdate, db: db_dependency, user: user_dependency):
    if user['is_admin']:
        emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

        # Apply only provided fields
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(emp, key, value)

        db.commit()
        db.refresh(emp)
        return emp
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")



# Delete Employee
@router.delete("/{employee_id}")
async def delete_employee(employee_id: int, db: db_dependency, user : user_dependency):
    if user['is_admin']:
        emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        db.delete(emp)
        db.commit()
        return {"Message":"Employee Deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
