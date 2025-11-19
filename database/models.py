from sqlalchemy import (
    Column, Integer, String, Date, Float, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# -------------------------
# Department Table
# -------------------------
class Department(Base):
    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=False, unique=True)

    employees = relationship("Employee", back_populates="department")


# -------------------------
# Role Table
# -------------------------
class Role(Base):
    __tablename__ = 'role'

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(100), nullable=False, unique=True)

    employees = relationship("Employee", back_populates="role")


# -------------------------
# Employee Table
# -------------------------
class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    joining_date = Column(Date, nullable=False)
    address = Column(String(255))
    password = Column(String(255), nullable=False)
    isadmin = Column(Boolean, nullable=False)

    fk_department_id = Column(Integer, ForeignKey('department.department_id'))
    fk_role_id = Column(Integer, ForeignKey('role.role_id'))
    fk_manager_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=True)

    department = relationship("Department", back_populates="employees")
    role = relationship("Role", back_populates="employees")
    manager = relationship("Employee", remote_side=[employee_id], backref="subordinates")

    # Relationships to other tables
    payslips = relationship("Payslip", back_populates="employee")
    salaries = relationship("Salary", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")
    regularizations = relationship("Regularization", foreign_keys="[Regularization.fk_employee_id]", back_populates="employee")
    leaves = relationship("Leave", back_populates="employee")
    leave_applications = relationship("LeaveApplication", foreign_keys="[LeaveApplication.fk_employee_id]", back_populates="employee")
    expense_claims = relationship("ExpenseClaim", foreign_keys="[ExpenseClaim.fk_employee_id]", back_populates="employee")


# -------------------------
# Expense Claim Table
# -------------------------
class ExpenseClaim(Base):
    __tablename__ = 'expense_claim'

    claim_id = Column(Integer, primary_key=True, autoincrement=True)
    claim_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)

    fk_employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    fk_manager_id = Column(Integer, ForeignKey('employee.employee_id'))

    employee = relationship("Employee", foreign_keys=[fk_employee_id], back_populates="expense_claims")
    manager = relationship("Employee", foreign_keys=[fk_manager_id])


# -------------------------
# Payslip Table
# -------------------------
class Payslip(Base):
    __tablename__ = 'payslip'

    payslip_id = Column(Integer, primary_key=True, autoincrement=True)
    basic_amount = Column(Float, nullable=False)
    hra = Column(Float)
    special_allowance = Column(Float)
    internet_allowance = Column(Float)
    payslip_month = Column(Date, nullable=False)

    fk_employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship("Employee", back_populates="payslips")


# -------------------------
# Salary Table
# -------------------------
class Salary(Base):
    __tablename__ = 'salary'

    salary_id = Column(Integer, primary_key=True, autoincrement=True)
    lpa = Column(Float, nullable=False)

    fk_employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship("Employee", back_populates="salaries")


# -------------------------
# Attendance Table
# -------------------------
class Attendance(Base):
    __tablename__ = 'attendance'

    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    punch_time = Column(Date, nullable=False)

    fk_employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship("Employee", back_populates="attendances")


# -------------------------
# Regularization Table
# -------------------------
class Regularization(Base):
    __tablename__ = 'regularization'

    regularization_id = Column(Integer, primary_key=True, autoincrement=True)
    regularization_date = Column(Date, nullable=False)
    regularization_reason = Column(String(255))

    fk_employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    fk_manager_id = Column(Integer, ForeignKey('employee.employee_id'))

    employee = relationship("Employee", foreign_keys=[fk_employee_id], back_populates="regularizations")
    manager = relationship("Employee", foreign_keys=[fk_manager_id])


# -------------------------
# Leave Table
# -------------------------
class Leave(Base):
    __tablename__ = 'leave'

    leave_id = Column(Integer, primary_key=True, autoincrement=True)
    assign_year = Column(Integer)
    casual_leave = Column(Integer)
    plan_leave = Column(Integer)
    probation_leave = Column(Integer)
    sick_leave = Column(Integer)
    total_leave = Column(Integer)
    balance_leave = Column(Integer)

    fk_employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship("Employee", back_populates="leaves")


# -------------------------
# Leave Application Table
# -------------------------
class LeaveApplication(Base):
    __tablename__ = 'leave_application'

    leave_application_id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Integer)
    fk_status = Column(String(50))  # Assuming status is a string or enum

    fk_employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    fk_manager_id = Column(Integer, ForeignKey('employee.employee_id'))

    employee = relationship("Employee", foreign_keys=[fk_employee_id], back_populates="leave_applications")
