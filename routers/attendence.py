from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date, time
from database.models import Attendance
from routers.auth import db_dependency, user_dependency

router = APIRouter(prefix="/attendance", tags=["Attendance"])


class AttendanceBase(BaseModel):
    punch_time: date

class AttendanceCreate(BaseModel):
    pass

class AttendanceUpdate(BaseModel):
    punch_time: datetime

class AttendanceResponse(BaseModel):
    attendance_id: int
    punch_time: datetime
    fk_employee_id: int

    class Config:
        orm_mode = True



@router.post("/", response_model=AttendanceResponse)
def create_attendance(db: db_dependency, user: user_dependency):
    current_time = datetime.now()
    employee_id = user["id"]

    new_attendance = Attendance(
        punch_time=current_time,
        fk_employee_id=employee_id
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance



@router.get("/date/{punch_date}", response_model=list[AttendanceResponse])
def get_attendance_by_date(
    punch_date: date,
    db: db_dependency,
    user: user_dependency
):
    start_dt = datetime.combine(punch_date, time.min)
    end_dt = datetime.combine(punch_date, time.max)

    return db.query(Attendance).filter(
        Attendance.fk_employee_id == user["id"],
        Attendance.punch_time >= start_dt,
        Attendance.punch_time <= end_dt
    ).all()




@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db: db_dependency,
    user: user_dependency
):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Only admin can update attendance")

    record = db.query(Attendance).filter(
        Attendance.attendance_id == attendance_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    record.punch_time = attendance_data.punch_time

    db.commit()
    db.refresh(record)
    return record




@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: db_dependency,
    user: user_dependency
):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Only admin can delete attendance")

    record = db.query(Attendance).filter(
        Attendance.attendance_id == attendance_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    db.delete(record)
    db.commit()

    return {"message": "Attendance deleted successfully"}

