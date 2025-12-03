from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import Annotated
from datetime import timedelta, datetime, timezone
from database.models import Employee
from database.database import engine,sessionlocal as SessionLocal
import os
from dotenv import load_dotenv
load_dotenv()


auth_router = APIRouter(prefix='/auth', tags=['Authentication'] )

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY","d2e2b8fe4827c93ad7ac831a45b2f28c6f33e04f975c0b4b2b1b8d8b38d694a4") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class Token(BaseModel):
    access_token: str
    token_type: str

# Database dependency
def get_db():  # pragma: no cover
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authenticate user
def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Employee).filter(Employee.email == email).first()
    if not user or not (password == user.password):
        return None  # pragma: no cover
    return user

# Create JWT token
def create_access_token(email: str, employee_id: int, is_admin: bool, expires_delta: timedelta):
    encode = {
        'email': email,
        'emp_id': employee_id,
        'is_admin': is_admin
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Get current user from token
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('email')
        employee_id: int = payload.get('emp_id')
        is_admin: bool = payload.get('is_admin')
        if email is None or employee_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.') # pragma: no cover
        return {'email': email, 'id': employee_id, 'is_admin': is_admin}
    except JWTError: # pragma: no cover
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')



db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@auth_router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password', headers={"WWW-Authenticate": "Bearer"})  # pragma: no cover
    
    # Create JWT token
    token = create_access_token(user.email, user.employee_id,user.isadmin, timedelta(minutes=60))
    
    # Update last_login
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    return {
        'access_token': token,
        'token_type': 'bearer',
    }



