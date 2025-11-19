from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Role
from routers.auth import user_dependency, db_dependency
from pydantic import BaseModel

router = APIRouter(prefix="/roles", tags=["Roles"])


class RoleBase(BaseModel):
    role: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleResponse(RoleBase):
    role_id: int

    class Config:
        from_attributes = True


# ➤ Create Role
@router.post("/", response_model=RoleResponse)
def create_role(role_data: RoleCreate, db: db_dependency, user: user_dependency):
    if user['is_admin']:
        existing_role = db.query(Role).filter(Role.role == role_data.role).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="Role already exists")

        new_role = Role(role=role_data.role)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only users with administrator privileges can create new role.")
    return new_role


# ➤ Get All Roles
@router.get("/", response_model=list[RoleResponse])
def get_roles(db: db_dependency, user:user_dependency):
    return db.query(Role).all()


# ➤ Get Role By ID
@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: db_dependency, user:user_dependency):
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# ➤ Update Role by ID
@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_data: RoleUpdate, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        # Check duplicate role name
        duplicate = db.query(Role).filter(Role.role == role_data.role, Role.role_id != role_id).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Role with same name already exists")

        role.role = role_data.role
        db.commit()
        db.refresh(role)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return role


# ➤ Update Role by role
@router.put("/update_role_by_name/{role_name}", response_model=RoleResponse)
def update_role_by_name(role_name: str, role_data: RoleUpdate, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        role = db.query(Role).filter(Role.role == role_name).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        # Check duplicate role name
        duplicate = db.query(Role).filter(Role.role == role_data.role).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Role with same name already exists")

        role.role = role_data.role
        db.commit()
        db.refresh(role)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return role


# ➤ Delete Role
@router.delete("/{role_id}")
def delete_role(role_id: int, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        role = db.query(Role).filter(Role.role_id == role_id).first()

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        db.delete(role)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    
    return {"message": "Role deleted successfully"}


# ➤ Delete Role by role
@router.delete("/delete_role_by_name/{role_name}", response_model=RoleResponse)
def delete_role_by_name(role_name: str, db: db_dependency, user:user_dependency):
    if user['is_admin']:
        role = db.query(Role).filter(Role.role == role_name).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        db.delete(role)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have sufficient permissions to perform this action")
    return role