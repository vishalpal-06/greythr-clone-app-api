import bcrypt
from datetime import date
from database.database import sessionlocal as SessionLocal
from database.models import (
    Department,
    Role,
    Employee,
    ExpenseClaim,
    Salary,
    Regularization,
)  # Import your SQLAlchemy models


def seed_data():
    """Seed initial data into RDS MySQL"""

    # Create session
    db = SessionLocal()

    try:
        # Clear existing data (in reverse foreign key order)
        db.query(ExpenseClaim).delete()
        db.query(Salary).delete()
        db.query(Regularization).delete()
        db.query(Employee).delete()
        db.query(Role).delete()
        db.query(Department).delete()
        db.commit()
        print("🗑️  Cleared all tables")

        # 1. Insert Departments
        departments = [
            Department(department_name="Human Resources"),
            Department(department_name="Finance"),
            Department(department_name="Engineering"),
            Department(department_name="Sales"),
        ]
        db.add_all(departments)
        db.commit()
        print(f"✅ Inserted {len(departments)} departments")

        # 2. Insert Roles
        roles = [
            Role(role="Manager"),
            Role(role="Developer"),
            Role(role="Accountant"),
            Role(role="HR Executive"),
        ]
        db.add_all(roles)
        db.commit()
        print(f"✅ Inserted {len(roles)} roles")

        # 3. Insert Employees
        employees_data = [
            Employee(
                first_name="Vishu",
                last_name="Pal",
                email="vishalpal0602@gmail.com",
                joining_date=date(2023, 5, 18),
                address="Kalyan(E) Thane, Maharastra",
                fk_department_id=2,  # Engineering
                fk_role_id=1,  # Developer
                fk_manager_id=None,
                isadmin=1,
                password="Testing",  # Use bcrypt.hashpw in production
            ),
            Employee(
                first_name="John",
                last_name="Doe",
                email="john.doe123@example.com",
                joining_date=date(2023, 1, 15),
                address="123 Main Street, New York",
                fk_department_id=1,  # HR
                fk_role_id=2,  # Manager
                fk_manager_id=1,
                isadmin=0,
                password="Testing",
            ),
            Employee(
                first_name="Alice",
                last_name="Smith",
                email="alice.smith@example.com",
                joining_date=date(2023, 2, 10),
                address="456 Park Avenue, Chicago",
                fk_department_id=2,
                fk_role_id=1,
                fk_manager_id=1,
                isadmin=0,
                password="Testing",
            ),
            Employee(
                first_name="Robert",
                last_name="Brown",
                email="robert.brown@example.com",
                joining_date=date(2023, 3, 5),
                address="789 Broadway, Los Angeles",
                fk_department_id=1,
                fk_role_id=3,
                fk_manager_id=2,
                isadmin=0,
                password="Testing",
            ),
            Employee(
                first_name="Emily",
                last_name="Johnson",
                email="emily.johnson@example.com",
                joining_date=date(2023, 4, 20),
                address="101 Pine Street, San Francisco",
                fk_department_id=3,
                fk_role_id=2,
                fk_manager_id=2,
                isadmin=0,
                password="Testing",
            ),
            Employee(
                first_name="David",
                last_name="Williams",
                email="david.williams@example.com",
                joining_date=date(2023, 5, 18),
                address="202 Oak Street, Seattle",
                fk_department_id=2,
                fk_role_id=1,
                fk_manager_id=1,
                isadmin=0,
                password="Testing",
            ),
        ]

        inserted_count = 0
        for emp in employees_data:
            # Check duplicate email
            existing = db.query(Employee).filter(Employee.email == emp.email).first()
            if existing:
                print(f"⏭️  Skipping duplicate: {emp.email}")
                continue

            db.add(emp)
            inserted_count += 1

        db.commit()
        print(f"✅ Inserted {inserted_count} employees")

        print("🎉 Seeding complete!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
