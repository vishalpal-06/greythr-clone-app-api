from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Department
from routers.auth import user_dependency, db_dependency
from pydantic import BaseModel

router = APIRouter(prefix="/departments", tags=["Department"])


class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    department_id: int
    

    class Config:
        from_attributes = True


# ➤ Create Department
@router.post("/", response_model=DepartmentResponse)
def create_department(department_data: DepartmentCreate, db: db_dependency, user: user_dependency):
    if user['is_admin']:
        existing_department = db.query(Department).filter(Department.department_name == department_data.department_name).first()
        if existing_department:
            raise HTTPException(status_code=400, detail="Department already exists")

        new_department = Department(department_name=department_data.department_name)
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only users with administrator privileges can create new department.")
    return new_department


# ➤ Get All departments
@router.get("/", response_model=list[DepartmentResponse])
def get_departments(db: db_dependency, user:user_dependency):
    return db.query(Department).all()


# ➤ Get Department By ID
@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int, db: db_dependency, user:user_dependency):
    department_name = db.query(Department).filter(Department.department_id == department_id).first()
    if not department_name:
        raise HTTPException(status_code=404, detail="Department not found")
    return department_name


# ➤ Update Department by ID
@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int, department_data: DepartmentUpdate, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        department_name = db.query(Department).filter(Department.department_id == department_id).first()
        if not department_name:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

        # Check duplicate department_name name
        duplicate = db.query(Department).filter(Department.department_name == department_data.department_name, Department.department_id != department_id).first()
        if duplicate:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department with same name already exists")

        department_name.department_name = department_data.department_name
        db.commit()
        db.refresh(department_name)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return department_name


# ➤ Update Department by department_name
@router.put("/update_department_by_name/{department_name}", response_model=DepartmentResponse)
def update_department_by_name(department_name: str, department_data: DepartmentUpdate, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        department_name = db.query(Department).filter(Department.department_name == department_name).first()
        if not department_name:
            raise HTTPException(status_code=404, detail="Department not found")

        # Check duplicate department_name name
        duplicate = db.query(Department).filter(Department.department_name == department_data.department_name).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Department with same name already exists")

        department_name.department_name = department_data.department_name
        db.commit()
        db.refresh(department_name)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return department_name


# ➤ Delete Department
@router.delete("/{department_id}")
def delete_department(department_id: int, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        department = db.query(Department).filter(Department.department_id == department_id).first()

        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        db.delete(department)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    
    return {"message": f"Department {department.department_name} deleted successfully"}


# ➤ Delete Department by department_name
@router.delete("/delete_department_by_name/{department_name}")
def delete_department_by_name(department_name: str, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        department = db.query(Department).filter(Department.department_name == department_name).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        db.delete(department)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return {"message": f"Department {department_name} deleted successfully"}