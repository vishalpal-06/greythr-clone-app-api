from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Enum
from database.models import Salary, Employee, Status
from routers.auth import user_dependency, db_dependency
from pydantic import BaseModel
from datetime import date
from sqlalchemy import Date, cast, func


router = APIRouter(prefix="/salary", tags=["Salary"])



class SalaryBase(BaseModel):
    lpa: int
    salary_year: int
    employee_id: int


class CreateSalary(SalaryBase):
    pass

class UpdateSalary(SalaryBase):
    pass


@router.post("/create_salary")
async def create_salary(salary_data:CreateSalary, db: db_dependency, user : user_dependency):
    if not user['is_admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")

    salary = db.query(Salary).filter(Salary.fk_employee_id == salary_data.employee_id,Salary.salary_year == salary_data.salary_year).first()
    if salary:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Salary already exists for this employee for the specified year.")
    
    employee = db.query(Employee).filter(Employee.employee_id == salary_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    new_salary = Salary(
        lpa = salary_data.lpa,
        salary_year = salary_data.salary_year,
        fk_employee_id = salary_data.employee_id
    )
    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)
    return new_salary
        

@router.get("/get_salary_by_year")
async def get_salary_by_year(salary_year:int, db: db_dependency, user : user_dependency):
    salary = db.query(Salary).filter(Salary.fk_employee_id == user['id'], Salary.salary_year == salary_year).first()
    if not salary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found salary for year {salary_year}.")
    return salary


@router.get("/get_all_salarys")
async def get_salary_by_employee(db: db_dependency, user : user_dependency):
    salary = db.query(Salary).filter(Salary.fk_employee_id == user['id']).all()
    if not salary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found salary")
    return salary









