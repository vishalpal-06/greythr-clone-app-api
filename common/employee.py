
from database.models import Employee
from fastapi import HTTPException, status
from schema.employee_schema import EmployeeCreate, EmployeeUpdate
from typing import List
from routers.auth import db_dependency, user_dependency



def get_all_employees_common(db: db_dependency, user: user_dependency):
    if user['is_admin']:
        return db.query(Employee).all()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")



def get_my_details_common(db: db_dependency, user: user_dependency):
    emp = db.query(Employee).filter(Employee.employee_id == user['id']).first()
    if emp is None:
        raise HTTPException(status_code=404, detail="Details not found")
    return emp



def get_employee_by_id_common(employee_id: int, db:db_dependency, user:user_dependency):
    if not user['is_admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp
        
    

def get_employee_by_email_common(employee_email: str, db:db_dependency, user:user_dependency):
    if not user['is_admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    emp = db.query(Employee).filter(Employee.email == employee_email).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp
        
    

def get_employee_by_id_for_manager_common(employee_id: int, db:db_dependency, user:user_dependency):
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    if not emp.fk_manager_id == user['id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found in Your Under")
    return emp
        
    

def get_employee_by_email_for_manager_common(employee_email: str, db:db_dependency, user:user_dependency):
    emp = db.query(Employee).filter(Employee.email == employee_email).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    if not emp.fk_manager_id == user['id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found in Your Under")
    return emp
    



def create_employee_common(employee:EmployeeCreate, db:db_dependency, user:user_dependency):
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



def update_employee_using_id_common(employee_id: int, updated_employee_date: EmployeeUpdate, db: db_dependency, user: user_dependency):
    if not user['is_admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    # Apply only provided fields
    for key, value in updated_employee_date.model_dump(exclude_unset=True).items():
        setattr(emp, key, value)

    db.commit()
    db.refresh(emp)
    return emp
        


def update_employee_using_email_common(employee_email: str, updated_employee_date: EmployeeUpdate, db: db_dependency, user: user_dependency):
    if not user['is_admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    
    emp = db.query(Employee).filter(Employee.email == employee_email).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    # Apply only provided fields
    for key, value in updated_employee_date.model_dump(exclude_unset=True).items():
        setattr(emp, key, value)

    db.commit()
    db.refresh(emp)
    return emp



def delete_employee_using_id_common(employee_id: int, db: db_dependency, user : user_dependency):
    if user['is_admin']:
        emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        db.delete(emp)
        db.commit()
        return {"Message":"Employee Deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")



def delete_employee_using_email_common(employee_email: str, db: db_dependency, user : user_dependency):
    if user['is_admin']:
        emp = db.query(Employee).filter(Employee.email == employee_email).first()
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        db.delete(emp)
        db.commit()
        return {"Message":"Employee Deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")

