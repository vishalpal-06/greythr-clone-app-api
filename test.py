import sqlite3
import bcrypt
from datetime import date

# Connect to the SQLite database
conn = sqlite3.connect('greythr.db')
cursor = conn.cursor()
# -------------------------
# 1. Insert Departments
# -------------------------
departments = [
    ("Human Resources",),
    ("Finance",),
    ("Engineering",),
    ("Sales",)
]

cursor.executemany("INSERT INTO department (department_name) VALUES (?)", departments)
print(f"✅ Inserted {len(departments)} departments.")

# -------------------------
# 2. Insert Roles
# -------------------------
roles = [
    ("Manager",),
    ("Developer",),
    ("Accountant",),
    ("HR Executive",)
]

cursor.executemany("INSERT INTO role (role) VALUES (?)", roles)
print(f"✅ Inserted {len(roles)} roles.")

# -------------------------
# 3. Insert Employees
# -------------------------

employees_data = [
    ["John", "Doe", "john.doe123@example.com", date(2023, 1, 15), "123 Main Street, New York", 1, 2, None],
    ["Alice", "Smith", "alice.smith@example.com", date(2023, 2, 10), "456 Park Avenue, Chicago", 2, 1, 1],
    ["Robert", "Brown", "robert.brown@example.com", date(2023, 3, 5), "789 Broadway, Los Angeles", 1, 2, 1],
    ["Emily", "Johnson", "emily.johnson@example.com", date(2023, 4, 20), "101 Pine Street, San Francisco", 3, 2, 2],
    ["David", "Williams", "david.williams@example.com", date(2023, 5, 18), "202 Oak Street, Seattle", 2, 1, 2]
]



insert_query = """
INSERT INTO employee (first_name, last_name, email, joining_date, address, fk_department_id, fk_role_id, fk_manager_id, password)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    cursor.execute(insert_query, (
        emp[0], emp[1], emp[2], emp[3],
        default_hire_date if emp[4] is None else emp[4],
        emp[5], emp[6], emp[7], "Testing"
    ))
    inserted_count += 1

# # Commit changes
conn.commit()
print(f"✅ Inserted {inserted_count} employees. Skipped {skipped_count} duplicates.")

# Close connection
conn.close()