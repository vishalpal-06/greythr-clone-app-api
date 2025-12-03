import sqlite3
import bcrypt
from datetime import date

# Connect to the SQLite database
conn = sqlite3.connect("greythr.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM department")
cursor.execute("DELETE FROM role")
cursor.execute("DELETE FROM employee")
cursor.execute("DELETE FROM regularization")
cursor.execute("DELETE FROM salary")
cursor.execute("DELETE FROM expense_claim")
# -------------------------
# 1. Insert Departments
# -------------------------
departments = [("Human Resources",), ("Finance",), ("Engineering",), ("Sales",)]

cursor.executemany("INSERT INTO department (department_name) VALUES (?)", departments)
print(f"✅ Inserted {len(departments)} departments.")

# -------------------------
# 2. Insert Roles
# -------------------------
roles = [("Manager",), ("Developer",), ("Accountant",), ("HR Executive",)]

cursor.executemany("INSERT INTO role (role) VALUES (?)", roles)
print(f"✅ Inserted {len(roles)} roles.")

# -------------------------
# 3. Insert Employees
# -------------------------

employees_data = [
    [
        "Vishu",
        "Pal",
        "vishalpal0602@gmail.com",
        date(2023, 5, 18),
        "Kalyan(E) Thane, Maharastra",
        2,
        1,
        None,
        1,
    ],
    [
        "John",
        "Doe",
        "john.doe123@example.com",
        date(2023, 1, 15),
        "123 Main Street, New York",
        1,
        2,
        1,
        0,
    ],
    [
        "Alice",
        "Smith",
        "alice.smith@example.com",
        date(2023, 2, 10),
        "456 Park Avenue, Chicago",
        2,
        1,
        1,
        0,
    ],
    [
        "Robert",
        "Brown",
        "robert.brown@example.com",
        date(2023, 3, 5),
        "789 Broadway, Los Angeles",
        1,
        2,
        2,
        0,
    ],
    [
        "Emily",
        "Johnson",
        "emily.johnson@example.com",
        date(2023, 4, 20),
        "101 Pine Street, San Francisco",
        3,
        2,
        2,
        0,
    ],
    [
        "David",
        "Williams",
        "david.williams@example.com",
        date(2023, 5, 18),
        "202 Oak Street, Seattle",
        2,
        1,
        2,
        0,
    ],
]


insert_query = """
INSERT INTO employee (first_name, last_name, email, joining_date, address, fk_department_id, fk_role_id, fk_manager_id, isadmin, password)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

default_hire_date = date.today().isoformat()
inserted_count = 0
skipped_count = 0

for emp in employees_data:
    # Check for duplicate email
    # cursor.execute("SELECT email FROM employee WHERE email = ?", (emp[2],))
    if cursor.fetchone():
        print(f"Skipping duplicate email: {emp[2]}")
        skipped_count += 1
        continue

    # Insert employee
    cursor.execute(
        insert_query,
        (
            emp[0],
            emp[1],
            emp[2],
            emp[3],
            emp[4],
            emp[5],
            emp[6],
            emp[7],
            emp[8],
            "Testing",
        ),
    )
    inserted_count += 1

# # Commit changes
conn.commit()
print(f"✅ Inserted {inserted_count} employees. Skipped {skipped_count} duplicates.")

# Close connection
conn.close()
