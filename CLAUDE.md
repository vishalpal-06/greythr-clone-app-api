---
noteId: "342ab7e073ac11f19a53156b6722f380"
tags: []

---

# CLAUDE.md

This repository implements a Greythr/greytHR HR-platform clone exposed as a FastAPI service backed by SQLAlchemy and validated through Pydantic. The application covers core HR operations — employees, departments, roles, attendance, regularization, leave (allocation + applications), payroll (salary + payslips), and expense claims — with three role-scoped API surfaces (`/admin`, `/manager`, `/user`) authenticated via JWT bearer tokens. A pair of MCP companion scripts (`mcp_server.py`, `mcp_client.py`) plus a Streamlit UI (`ui_app.py`) expose the same FastAPI surface as tools to Claude / Google Gemini agents.

## Tech Stack

### Core Framework
- **Python**: 3.12 (pinned in `Dockerfile` via `python:3.12-slim`; CI uses 3.12)
- **FastAPI**: 0.124.0
- **Uvicorn**: 0.38.0 (ASGI server, listens on port 8000)
- **Starlette**: 0.50.0

### Data Layer
- **SQLAlchemy**: 2.0.27 (synchronous, declarative `Base`)
- **SQLite**: built-in stdlib driver — local/dev DB at `sqlite:///./greythr.db`
- **PyMySQL**: MySQL driver for production RDS
- **greenlet**: 3.3.0

> **Gotcha**: SQLAlchemy is configured *synchronously* even though Uvicorn is async. No `aiomysql`/`asyncpg` is wired up. Calls block the event loop; be aware under high concurrency.

### Validation & Serialization
- **Pydantic**: 2.11.7 (+ `pydantic-settings` 2.5.2, `pydantic_core` 2.33.2)
- **email-validator**: 2.3.0
- **python-multipart**: 0.0.20
- **openapi-pydantic**: 0.5.1

### Auth & Security
- **PyJWT**: 2.10.1 (HS256)
- **python-jose**: 3.5.0
- **bcrypt**: 5.0.0 (via **passlib** 1.7.4)
- **Authlib**: 1.6.5
- **cryptography**: 46.0.3, **rsa**: 4.9.1, **ecdsa**: 0.19.1

### Testing & Quality
- **pytest**: 9.0.2, **pytest-cov**: 7.0.0, **coverage**: 7.12.0
- **black**: 25.11.0 (no `pyproject.toml`/`setup.cfg` overrides — defaults only)
- **mypy_extensions**: 1.1.0

### MCP / LLM Integration
- **mcp**: 1.22.0, **fastmcp**: 2.13.3
- **langchain-anthropic**, **langchain-google-genai**, **langchain-mcp-adapters**, **langgraph** (used by `mcp_client.py` / `ui_app.py`)
- **streamlit** (used by `ui_app.py`)

### Observability & Utilities
- **sentry-sdk**: 2.47.0 (available but no obvious init call in app code)
- **python-dotenv**: 1.2.1, **httpx**: 0.28.1, **requests**: 2.32.5, **rich**: 14.2.0
- **fastapi-cli**: 0.0.16, **typer**: 0.20.0, **uv**: 0.9.16

## Directory Structure

```
greythr-clone-app-api/
├── main.py                                 # FastAPI app entry point (~40 lines)
├── mcp_server.py                           # FastMCP wrapper exposing FastAPI as MCP tools
├── mcp_client.py                           # Claude (Sonnet 4.5) LangGraph agent over MCP
├── ui_app.py                               # Streamlit chatbot using Google Gemini 2.5 Flash
├── insert_db_data.py                       # Production RDS seeder (bcrypt-hashed passwords)
├── test_db_conn.py                         # MySQL connection sanity-check utility
│
├── routers/                                # API route handlers, organized by role
│   ├── auth.py                             # /auth/token, /auth/login_json, JWT helpers
│   ├── admin/                              # /admin/* endpoints
│   │   ├── admin_api.py                    #   - aggregator
│   │   ├── admin_employee_api.py
│   │   ├── admin_role_api.py
│   │   ├── admin_department_api.py
│   │   ├── admin_attendance_api.py
│   │   ├── admin_salary_api.py
│   │   ├── admin_leave_api.py
│   │   ├── admin_regularization_api.py
│   │   ├── admin_payslip_api.py
│   │   ├── admin_leave_application_api.py
│   │   └── admin_expense_claim_api.py
│   ├── manager/                            # /manager/* endpoints
│   │   ├── manager_api.py                  #   - aggregator
│   │   ├── manager_employee_api.py
│   │   ├── manager_attendance_api.py
│   │   ├── manager_leave_api.py
│   │   ├── manager_leave_application_api.py
│   │   ├── manager_expense_claim_api.py
│   │   └── manager_regularization_api.py
│   └── user/                               # /user/* endpoints (mostly /user/my/*)
│       ├── user_api.py                     #   - aggregator
│       ├── user_employee_api.py
│       ├── user_attendance_api.py
│       ├── user_department_api.py
│       ├── user_salary_api.py
│       ├── user_leave_api.py
│       ├── user_leave_application_api.py
│       ├── user_payslip_api.py
│       ├── user_regularization_api.py
│       ├── user_expense_claim_api.py
│       └── user_role_api.py
│
├── database/
│   ├── database.py                         # Engine setup, sessionlocal, Base, env switching
│   ├── models.py                           # SQLAlchemy ORM models (~216 lines)
│   ├── common.py                           # hash_password / verify_password (bcrypt)
│   └── __init__.py
│
├── schema/                                 # Pydantic v2 schemas (Base/Create/Update/Response)
│   ├── employee_schema.py
│   ├── attendance_schema.py
│   ├── department_schema.py
│   ├── salary_schema.py
│   ├── leave_schema.py
│   ├── leave_application_schema.py
│   ├── payslip_schema.py
│   ├── regularization_schema.py
│   ├── expense_claim_schema.py
│   └── role_schema.py
│
├── common/                                 # Business logic between routers and DB
│   ├── common.py                           # _require_admin() — single admin-check helper
│   ├── attendance.py
│   ├── employee.py
│   ├── department.py
│   ├── expense_claim.py
│   ├── leave.py
│   ├── leave_application.py
│   ├── payslip.py
│   ├── regularization.py
│   ├── salary.py
│   └── role.py
│
├── tests/
│   ├── conftest.py                         # db_session, client, role tokens, read_json fixtures
│   ├── seed_db.py                          # seed_all_tables() — loads JSON test data
│   ├── test_data/                          # *.json seed fixtures (departments, employees, ...)
│   ├── expected_responses/                 # admin/, manager/, user/ snapshot JSONs
│   └── test_cases/
│       ├── test_health.py
│       ├── test_admin_api/                 # 10 files
│       ├── test_manager_api/
│       └── test_user_api/
│
├── .github/workflows/ci.yaml               # Black -> pytest (100% cov) -> ECR -> ECS
├── .vscode/                                # launch.json (FastAPI + pytest), settings.json
├── .claude/commands/run-test.md            # Custom Claude Code command
├── Dockerfile                              # Python 3.12-slim, EXPOSE 8000, uvicorn CMD
├── ecs-task-def.json                       # AWS Fargate task definition
├── requirements.txt
├── pytest.ini                              # pythonpath = .
├── .coveragerc                             # omits seed/db/main/mcp/ui modules
├── .env                                    # secrets (currently committed — see Gotchas)
├── .dockerignore / .gitignore
├── greythr.db                              # SQLite dev DB
└── test_db.sqlite3                         # SQLite test DB (recreated per test session)
```

## Architecture

The application is a clean three-layer design:

1. **Routers** (`routers/`) — HTTP concerns, dependency injection, role-based path routing.
2. **Common / business logic** (`common/`) — authorization checks, CRUD orchestration, computed fields (e.g. leave-day arithmetic).
3. **Database** (`database/`) — SQLAlchemy engine/session/models.

### FastAPI Bootstrap (`main.py`)

- `main.py:10-14` — `FastAPI(title="Grethr Clone API 12345", version="1.2.0")`. **Note** the title typo; the welcome string at `main.py:19-21` reads `"Welcome to My Grehthrapp By Kishan"`. Don't "fix" without checking whether tests assert against it.
- `main.py:24-30` — CORS middleware: allows only `http://localhost:3000`, `allow_credentials=True`, methods/headers `*`.
- `main.py:33-36` — Router includes for `/auth`, `/admin`, `/manager`, `/user`.
- `main.py:38-39` — On import, `models.Base.metadata.create_all(bind=engine)` creates all tables. There is no Alembic; schema changes happen via model edits + DB recreate.

### Router Layering

Each role aggregator file pulls in feature sub-routers and is mounted at the role prefix:

| Mount | Aggregator | Sub-routers |
|---|---|---|
| `/auth` | `routers/auth.py:17` | login & token endpoints |
| `/admin` | `routers/admin/admin_api.py:16` | 10 sub-routers (employees, roles, departments, attendance, salary, leave, regularization, payslips, leave-applications, expense-claims) |
| `/manager` | `routers/manager/manager_api.py:12` | 6 sub-routers (subordinates, attendance, leave, regularization, leave-applications, expense-claims) |
| `/user` | `routers/user/user_api.py:16` | 10 sub-routers (mostly `/user/my/...`) |

### Dependency Injection

`database/database.py:1-43`:
- `DB_CONNECT` (env var) picks the engine. `"local"` (default) → SQLite `./greythr.db`. Anything else → MySQL via PyMySQL with `pool_pre_ping=True`, `pool_recycle=3600`, `pool_size=DB_POOL_SIZE` (default 10), `max_overflow=DB_MAX_OVERFLOW` (default 20).
- `sessionlocal = sessionmaker(autoflush=True, bind=engine)` (autocommit off).
- `Base = declarative_base()`.

`routers/auth.py:38-85`:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency   = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,    Depends(get_current_user)]
```
Every endpoint takes both, e.g. `routers/admin/admin_employee_api.py:21`:
```python
def list_all_employees_endpoint(db: db_dependency, user: user_dependency):
    return get_all_employees(db=db, user=user)
```

### Request Flow Example

`GET /admin/employees/`:
1. FastAPI resolves `db_dependency` (opens session) and `user_dependency` (decodes JWT).
2. Router (`admin_employee_api.py`) delegates to `common/employee.py:get_all_employees`.
3. `get_all_employees` calls `_require_admin(user)` (`common/common.py:4-8`) — raises 403 if `user["is_admin"]` is false.
4. SQLAlchemy `db.query(Employee).all()` runs synchronously.
5. FastAPI serializes via `response_model=List[EmployeeResponse]` (Pydantic with `from_attributes=True`).

Authorization is **not middleware**; it lives in `common/` and is per-function.

## Data Model

All tables are defined in `database/models.py` and inherit from `Base = declarative_base()` (line 14). A custom `Status` enum (`Pending`, `Approved`, `Rejected`) is declared both in `database/models.py` (SQLAlchemy column type) and per-schema in `schema/*` (Pydantic validation).

### Core Tables

#### `department`
| Column | Type | Notes |
|---|---|---|
| `department_id` | Integer PK, autoincrement | |
| `department_name` | String(100), unique, not null | |

Relationships: `employees` (1→N) → Employee.

#### `role`
| Column | Type | Notes |
|---|---|---|
| `role_id` | Integer PK, autoincrement | |
| `role` | String(100), unique, not null | |

Relationships: `employees` (1→N) → Employee.

#### `employee`
| Column | Type | Notes |
|---|---|---|
| `employee_id` | Integer PK, autoincrement | |
| `first_name` | String(50), not null | |
| `last_name` | String(50), not null | |
| `email` | String(100), unique, not null | |
| `joining_date` | DateTime, not null | |
| `address` | String(255) | |
| `password` | String(255), not null | **Plain-text in current login flow** — see Auth section |
| `isadmin` | Boolean, not null | Sole role flag |
| `fk_department_id` | Integer FK → department | |
| `fk_role_id` | Integer FK → role | |
| `fk_manager_id` | Integer FK → employee, nullable | Self-referencing (manager → subordinates) |

Relationships: `department`, `role`, `manager` (self), backref `subordinates`; one-to-many to `payslips`, `salaries`, `attendances`, `regularizations`, `leaves`, `leave_applications`, `expense_claims`.

### Payroll Tables

#### `salary`
- `salary_id` PK, `lpa` (Float, not null — Lakhs Per Annum), `salary_year` (Integer, not null), `fk_employee_id` FK.
- Application-layer uniqueness: one row per `(fk_employee_id, salary_year)`.

#### `payslip`
- `payslip_id` PK, `basic_amount` (Float, not null), `hra`, `special_allowance`, `internet_allowance` (Float).
- `payslip_month` (DateTime, not null) — schema validation forces 1st-of-month at 00:00:00.
- One row per `(fk_employee_id, payslip_month)` enforced in `common/payslip.py`.

> **Gotcha**: All monetary amounts use `Float`, not `Decimal`. Financial precision is at risk; treat as an existing bug, not a feature.

### Attendance / Regularization

#### `attendance`
- `attendance_id` PK, `punch_time` (DateTime, not null), `fk_employee_id` FK.
- **No duplicate-punch prevention** — multiple rows at the same time are allowed.
- **No present/absent status** — raw punch records only.

#### `regularization`
- Fields: `regularization_start_time`, `regularization_end_time`, `regularization_reason` (String(255)), `regularization_status` (Status enum, default Pending), `fk_employee_id`, `fk_manager_id`.
- Manager-of-record is locked in at creation time (`fk_manager_id = employee.fk_manager_id`).

### Leave

#### `leave` (annual allocation)
- `leave_id` PK, `assign_year`, plus integer counters: `casual_leave`, `plan_leave`, `probation_leave`, `sick_leave`, `total_leave`, `balance_leave`, `fk_employee_id`.
- One row per `(fk_employee_id, assign_year)` (application-layer only).
- `balance_leave` is **not auto-decremented** when applications are approved.

#### `leave_application`
- `from_date`, `end_date` (validated `end_date > from_date`), `total_days` (computed as `(end_date - from_date).days + 1` in `common/leave_application.py:33`), `leave_status` (Status), `leave_reason` (5–255 chars), `fk_employee_id`, `fk_manager_id`.
- Time component on the dates is ignored for the total-days calc.

### Expense

#### `expense_claim`
- `claim_id` PK, `claim_date` (DateTime, not null), `amount` (Float, not null), `description` (String(500), not null, 10–500 chars), `claim_status` (Status, default Pending), `fk_employee_id`, `fk_manager_id`.

### Schema Conventions (`schema/*.py`)

All Pydantic v2 modules follow:
- `*Base` — shared field definitions / validators
- `*Create` — POST body (often adds `fk_employee_id` or `password`)
- `*Update` — partial updates (typically all-optional)
- `*StatusUpdate` — for approval flows (single `*_status: Status` field)
- `*Response` — adds the PK + `model_config = ConfigDict(from_attributes=True)` so ORM instances serialize cleanly

Notable per-schema validations:
- `PayslipBase.payslip_month` — must be 1st of month at 00:00:00.
- `LeaveApplicationBase`, `RegularizationBase` — end > start; reason 5–255 chars.
- `ExpenseClaimBase` — `amount > 0`, description 10–500 chars.
- `SalaryBase` — `lpa > 0`, `salary_year` ∈ [2000, 2100].
- `LeaveBase` — `assign_year` ∈ [2000, 2100], all counters ≥ 0.

## API Surface

Route inventory by role. Prefixes are mounted in `main.py`.

### Admin (`/admin/*`)

Full CRUD across every domain. All endpoints call `_require_admin(user)` in `common/`.

#### `/admin/employees`
- `GET /` — list all
- `GET /id/{employee_id}` · `GET /email/{email}`
- `POST /` — create
- `PUT /id/{employee_id}` · `PUT /email/{email}`
- `DELETE /id/{employee_id}` · `DELETE /email/{email}`

#### `/admin/roles`
- `POST /` · `PUT /id/{role_id}` · `PUT /name/{current_name}` · `DELETE /id/{role_id}` · `DELETE /name/{role_name}`

#### `/admin/departments`
- `POST /` · `PUT /id/{department_id}` · `PUT /name/{current_name}` · `DELETE /id/{department_id}` · `DELETE /name/{department_name}`

#### `/admin/attendance`
- `GET /` · `GET /date/{punch_date}` · `GET /employee/{employee_id}/date/{punch_date}` · `GET /employee/{employee_id}`

#### `/admin/leaves`
- `GET /employee/{employee_id}/year/{year}` · `GET /employee/{employee_id}`
- `POST /` · `DELETE /{leave_id}` · `DELETE /employee/{employee_id}/year/{year}`

#### `/admin/leave-applications`
- `GET /{app_id}` · `GET /employee/{emp_id}` · `GET /month/{year}/{month}`
- `PUT /{app_id}/status`

#### `/admin/regularizations`
- `GET /{reg_id}` · `PUT /{reg_id}/status`

#### `/admin/expense-claims`
- `GET /{claim_id}` · `GET /employee/{emp_id}` · `GET /status/{status}` · `GET /month/{year}/{month}` · `GET /employee/{emp_id}/month/{year}/{month}`
- `PUT /{claim_id}/status`

#### `/admin/payslips`
- `POST /` · `GET /employee/{employee_id}` · `GET /month/{year}/{month}` · `GET /employee/{employee_id}/month/{year}/{month}`
- `DELETE /{payslip_id}` · `DELETE /employee/{employee_id}/month/{year}/{month}`

#### `/admin/salaries`
- `GET /year/{year}` · `GET /employee/{employee_id}/year/{year}` · `GET /employee/{employee_id}/salaries`
- `POST /` · `DELETE /{salary_id}` · `DELETE /employee/{employee_id}/year/{year}`

### Manager (`/manager/*`)

Scoped to direct reports via `employee.fk_manager_id == user["id"]`. No `is_admin` requirement — auth purely via subordinate ownership.

- `/manager/subordinates` — `GET /id/{employee_id}` · `GET /email/{email}`
- `/manager/attendance` — `GET /date/{punch_date}` · `GET /employee/{employee_id}/date/{punch_date}`
- `/manager/leaves` — `GET /employee/{employee_id}/year/{year}` · `GET /employee/{employee_id}`
- `/manager/leave-applications` — `GET /status/{status}` · `GET /month/{year}/{month}` · `GET /employee/{emp_id}` · `PUT /{app_id}/status`
- `/manager/regularizations` — `GET /pending` · `GET /{reg_id}` · `GET /employee/{employee_id}` · `PUT /{reg_id}/status`
- `/manager/expense-claims` — `GET /{claim_id}` · `GET /status/{status}` · `GET /month/{year}/{month}` · `GET /employee/{emp_id}/month/{year}/{month}` · `PUT /{claim_id}/status`

### User (`/user/*`, mostly under `/user/my`)

Self-service only. Ownership check is `record.fk_employee_id == user["id"]`.

- `/user/my` — `GET /me/`
- `/user/my/attendance` — `POST /` (punch in) · `GET /my` · `GET /my/date/{date_str}`
- `/user/my/leave` — `GET /year/{year}` · `GET /`
- `/user/my/leave-applications` — `POST /` · `DELETE /{app_id}` (Pending only) · `GET /status/{status}` · `GET /{app_id}` · `GET /month/{year}/{month}`
- `/user/my/regularizations` — `POST /` · `GET /` · `GET /{reg_id}` · `GET /month/{year}/{month}`
- `/user/my/expense-claims` — `POST /` · `DELETE /{claim_id}` (Pending only) · `GET /status/{status}` · `GET /{claim_id}` · `GET /month/{year}/{month}`
- `/user/my/payslips` — `GET /` · `GET /month/{year}/{month}`
- `/user/my/salary` — `GET /year/{year}` · `GET /`
- `/user/my/roles` — `GET /` · `GET /id/{role_id}` (read-only)
- `/user/my/departments` — `GET /` · `GET /id/{department_id}` (read-only)

### Health Check

- `GET /` — returns `{"status": "Welcome to My Grehthrapp By Kishan"}` (`main.py:19-21`).

## Authentication & Authorization

### JWT Configuration (`routers/auth.py`)

| Setting | Default | Env Var | Notes |
|---|---|---|---|
| `SECRET_KEY` | `d2e2b8fe4827c93ad7ac831a45b2f28c6f33e04f975c0b4b2b1b8d8b38d694a4` | `SECRET_KEY` | Hardcoded fallback — must override in prod |
| `ALGORITHM` | `HS256` | `ALGORITHM` | Symmetric HMAC-SHA256 |
| Token TTL | 60 minutes | — | `routers/auth.py:109` |

`oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")` (`routers/auth.py:25`).

### Login Endpoints

- `POST /auth/token` — accepts `OAuth2PasswordRequestForm` (form data, Swagger-compatible).
- `POST /auth/login_json` — accepts `LoginRequest` JSON (`username: EmailStr`, `password: str`).

Both return `{"access_token": "...", "token_type": "bearer"}`.

### Authentication Flow

1. `authenticate_user(email, password, db)` (`routers/auth.py:48-52`): `db.query(Employee).filter(Employee.email == email).first()` followed by `password == user.password`. **Plain-text comparison.**
2. `create_access_token` (`routers/auth.py:56-62`) encodes:
   ```python
   {"email": email, "emp_id": employee_id, "is_admin": is_admin, "exp": now + 60min}
   ```
3. `get_current_user` (`routers/auth.py:66-81`) decodes the Bearer token and returns:
   ```python
   {"email": email, "id": employee_id, "is_admin": is_admin}
   ```
   Decode failure → `HTTP 401`.

> **Security gotcha**: `database/common.py` provides `hash_password` / `verify_password` using `passlib` + bcrypt, and `bcrypt_context` is initialized in `routers/auth.py`, but the login path compares raw strings. `insert_db_data.py` writes bcrypt-hashed passwords. The result is that bcrypt-seeded users currently cannot log in via `/auth/token` — wire up hashing or seed plain-text for now.

### Permission Boundaries

| Role | Identification | Scope | Enforcement |
|---|---|---|---|
| Admin | `user["is_admin"] == True` | All records | `_require_admin()` in `common/common.py:4-8` |
| Manager | Implicit — any authenticated user | Direct reports only (`employee.fk_manager_id == user["id"]`) | Per-function checks in `common/*.py` |
| User | Implicit — any authenticated user | Own records only (`record.fk_employee_id == user["id"]`) | Per-function checks in `common/*.py` |

There is no `Role`-table-based RBAC at the auth layer — the `role` table is for organizational job titles, not access control.

### Other Security Notes

- HTTPS is not enforced; CORS allows only `http://localhost:3000`.
- The 404 returned for "not your subordinate" (`common/employee.py:123-131`) is by-design security-through-obscurity but obscures legitimate "not found" cases.

## Business Logic (`common/`)

Each module owns one domain and exposes employee/manager/admin variants of read/write operations. All admin operations call `_require_admin()`; manager operations verify `fk_manager_id`; user operations verify `fk_employee_id`.

### `common/common.py`
- `_require_admin(user: dict)` — single source of truth for admin checks. Raises `HTTP 403` if `user.get("is_admin")` is falsy.

### `common/employee.py`
- Admin: `get_all_employees`, `get_employee_by_{id,email}`, `create_employee`, `update_employee_by_{id,email}`, `delete_employee_by_{id,email}`.
- Manager: `get_subordinate_by_{id,email}` — guards on `employee.fk_manager_id == user["id"]`, returns 404 if mismatch.
- User: `get_current_user_employee`.
- Partial updates use `model_dump(exclude_unset=True)`. **Caveat**: no whitelist — admins can change `password`/`isadmin` via the same endpoint.

### `common/department.py`, `common/role.py`
- Public read; admin-only writes.
- Names are unique case-insensitively (`.ilike()`), trimmed.
- Self-exclusion check on updates allows case re-spelling.
- Hard delete only — no cascade handling; deleting a department/role can orphan employees.

### `common/attendance.py`
- Employee `POST` punch-in; admin and manager read variants for date/employee combinations.
- Same-day queries use `datetime.combine(date, time.min/.max)`.
- Manager attendance query at lines 55–60 returns an empty list (not 404) if the manager has no subordinates.
- `common/attendance.py:170` has a typo: "Employee Not Founds".

### `common/leave.py`
- One `Leave` row per `(employee, year)` (application-layer; no DB unique constraint).
- Tracks 5 categories + `total_leave` + `balance_leave`. None of these are automatically decremented on approval.

### `common/leave_application.py`
- `total_days = (end_date - from_date).days + 1` (line 33; ignores weekends/holidays).
- Application's `fk_manager_id` is locked to `employee.fk_manager_id` at creation (line 39).
- Status flow: Pending → Approved/Rejected. Only Pending applications are user-deletable.
- **No leave-balance check** on approval — leave can be approved against insufficient/zero balance.
- **No overlap check** — multiple overlapping leaves can co-exist as Approved.

### `common/expense_claim.py`
- `fk_manager_id` set to employee's manager at creation (line 33). Fails if employee has no manager (lines 27–28).
- Only Pending claims are user-deletable (line 46).
- Manager can update status only if `fk_manager_id == user["id"]`; admin can override.
- `updated_at = datetime.utcnow()` only on status change.
- **No budget/limit validation**. Amount is Float.

### `common/regularization.py`
- Same lock-in/status pattern as expense claims and leave applications.
- **No correlation with attendance** — approving a regularization does not modify attendance rows.
- start/end ordering is not validated in business logic (schema enforces it at the API boundary).

### `common/payslip.py`
- One payslip per `(employee, month)`; check at lines 20–32.
- No math validation (components ≥ 0 is enforced only at schema level), no link to `Salary`.

### `common/salary.py`
- One `Salary` row per `(employee, year)` (application-layer).
- `lpa` is Float; no range check beyond the schema's `> 0`.

### Cross-cutting Gotchas

| Issue | Where | Severity |
|---|---|---|
| No leave-balance check on approval | `leave_application.py` | High |
| No overlap detection on approved leaves | `leave_application.py` | High |
| Manager lock-in: reassigning employee's manager doesn't reroute pending approvals | `leave_application.py`, `expense_claim.py`, `regularization.py` | Medium |
| `Float` for money | `payslip.py`, `salary.py`, `expense_claim.py` | Medium |
| Hard delete everywhere (no soft delete, no audit trail) | All modules | Medium |
| `updated_at` populated only on status updates, never on `create_*` | All approval modules | Low |
| 404 returned where 403 would be more accurate | `employee.py` (manager scope) | Low |

## Development Workflow (PowerShell)

All commands assume the repo's bundled `venv/` directory and Python 3.12.

### Initial Setup

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the API Locally

Tables auto-create on startup (`models.Base.metadata.create_all(bind=engine)` in `main.py`).

```powershell
uvicorn main:app --reload
```

- App: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health: `GET /` → welcome string

### Seed the Database

- **Production / RDS** (destructive — clears and repopulates):
  ```powershell
  python insert_db_data.py
  ```
  Uses bcrypt to hash seeded employee passwords.
- **Tests** — automatic; `tests/conftest.py`'s `db_session` fixture calls `seed_all_tables()` from `tests/seed_db.py` against the JSON files in `tests/test_data/`.

### Format / Lint

```powershell
black --check .   # what CI runs (will fail the build on diff)
black .           # auto-format
```

There is no `pyproject.toml` for Black; defaults apply.

### VS Code

`.vscode/launch.json` exposes:
- `Python Debugger: FastAPI` — Uvicorn with `--reload`
- `Debug Pytest` — runs the suite under the debugger

`.vscode/settings.json` configures pytest with the `tests/` directory and `test_*.py` discovery.

## Testing

### Layout

```
tests/
├── conftest.py          # fixtures: db_session, client, role tokens, read_json
├── seed_db.py           # seed_all_tables(session, test_data_dir)
├── test_data/           # JSON inputs (departments.json, employees.json, ...)
├── expected_responses/  # snapshot JSONs under admin/, manager/, user/
└── test_cases/
    ├── test_health.py
    ├── test_admin_api/   # ~10 files
    ├── test_manager_api/
    └── test_user_api/
```

~31 test files total.

### Test DB

- `sqlite:///./test_db.sqlite3` — **hardcoded** in `tests/conftest.py:19`; ignores `.env`'s `DB_CONNECT`.
- The `db_session` fixture:
  1. `Base.metadata.drop_all(bind=engine)`
  2. `Base.metadata.create_all(bind=engine)`
  3. `seed_all_tables(session, TEST_DATA_DIR)`
  4. yields the session
  5. cleans up
- `client` fixture overrides `get_db` on the FastAPI app to use `TestingSessionLocal`.
- Role token fixtures: `admin_user`, `manager_A`, `manager_B`, `user_A1`, `user_A2`, `user_B1`, `user_B2` — each POSTs `/auth/token` to obtain a JWT.

### Snapshot Helper: `read_json`

`tests/conftest.py:132` reads the `UPDATE_TEST_DATA` env var (`"1" | "true" | "True" | "yes" | "YES"`).

- **Normal mode** — loads the file under `tests/expected_responses/...` and compares.
- **Update mode** — introspects the call stack to grab the current `response.json()` and *writes* it to the expected file.

To refresh snapshots:
```powershell
$env:UPDATE_TEST_DATA = "1"
pytest tests\test_cases\test_admin_api\test_admin_department_api.py
Remove-Item Env:UPDATE_TEST_DATA
```

### Common Test Commands

```powershell
pytest                                       # full suite
pytest -v                                    # verbose
pytest tests\test_cases\test_health.py       # one file
pytest -k "department" -v                    # filter
pytest -s --disable-warnings --maxfail=1     # interactive iteration
pytest --cov=. --cov-report=html             # write htmlcov/
pytest --cov=. --cov-report=term-missing
pytest --cov=. --cov-fail-under=100          # CI threshold
```

Open the HTML report on Windows:
```powershell
start htmlcov\index.html
```

### Coverage Configuration (`.coveragerc`)

```ini
[run]
omit =
    tests\seed_db.py
    insert_db_data.py
    test_db_conn.py
    database\common.py
    database\database.py
    mcp_server.py
    mcp_client.py
    ui_app.py
    main.py
```

> **Important**: CI enforces `--cov-fail-under=100`. New code must be fully covered, *unless* it lives in one of the omitted files. `main.py`, the DB engine config, and the MCP/Streamlit companion scripts are intentionally excluded.

### Simulating CI Locally

```powershell
black --check .
pytest --disable-warnings --maxfail=1 --cov=. --cov-fail-under=100
```

## Build & Deployment

### Dockerfile

- Base: `python:3.12-slim`
- Workdir: `/app`
- Steps: copy `requirements.txt` → `pip install` (no cache) → copy source → `EXPOSE 8000` → run uvicorn.
- CMD: `uvicorn main:app --host 0.0.0.0 --port 8000`

```powershell
docker build -t greythr-clone-api:latest .
docker run -p 8000:8000 greythr-clone-api:latest
```

### `.dockerignore`

Excludes `venv/`, `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.coverage`, `htmlcov/`, `.idea/`, `.vscode/`, `.DS_Store`, `.env`.

### ECS Task Definition (`ecs-task-def.json`)

- Family: `greythr-dev-task-definition`
- Network: `awsvpc` on AWS Fargate
- CPU/Mem: `256` units / `512` MB
- Execution Role: `arn:aws:iam::681526277210:role/ecsTaskExecutionRole`
- Container: `greythr-dev-con`, image replaced by CI, port `8000/tcp`, `essential: true`.
- **No environment variables in the task definition itself** — secrets must be injected elsewhere (Secrets Manager / parameter store) before this is safe in production.

### GitHub Actions (`.github/workflows/ci.yaml`)

Triggers: push or PR to `main`. Stages:

1. **format-check** — `black --check` (v25.11.0).
2. **test** — needs `format-check`. Sets up Python 3.12, installs `requirements.txt` + `pytest pytest-cov`, runs:
   ```
   pytest --disable-warnings --maxfail=1 --cov=. --cov-fail-under=100
   ```
3. **push-to-ecr** — needs `format-check` + `test`. Configures AWS creds, logs into ECR, builds Docker image tagged `:${GITHUB_SHA}` and `:latest`, pushes both.
4. **deploy-to-ecs** — needs `push-to-ecr`. Renders `ecs-task-def.json` with the new image URI and deploys via `aws-actions/amazon-ecs-deploy-task-definition`. `wait-for-service-stability` is disabled.

GitHub Secrets required: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `ECR_REPOSITORY`, `ECS_SERVICE_NAME`, `ECS_CLUSTER_NAME`, `ECS_CONTAINER_NAME`. The AWS account ID `681526277210` is hardcoded in the task definition's execution role ARN.

## Environment & Configuration

Variables are loaded from `.env` via `python-dotenv`.

### Database

| Variable | Default | Used In |
|---|---|---|
| `DB_CONNECT` | `"local"` | `database/database.py:11` — `"local"` → SQLite; anything else → MySQL |
| `DB_USER` | — | `database/database.py:22`, `test_db_conn.py:8` |
| `DB_PASSWORD` | — | `database/database.py:23`, `test_db_conn.py:9` |
| `DB_HOST` | — | `database/database.py:24`, `test_db_conn.py:10` |
| `DB_PORT` | — | `database/database.py:25`, `test_db_conn.py:11` |
| `DB_NAME` | — | `database/database.py:26`, `test_db_conn.py:12` |
| `DB_POOL_SIZE` | `10` | `database/database.py:37` |
| `DB_MAX_OVERFLOW` | `20` | `database/database.py:38` |

### Auth

| Variable | Default | Notes |
|---|---|---|
| `SECRET_KEY` | hardcoded hex string | `routers/auth.py:20-22` — override in prod |
| `ALGORITHM` | `HS256` | `routers/auth.py:23` |

### LLM / Tracing (loaded but consumed by SDKs, not by app code)

`ANTHROPIC_API_KEY` (used by `mcp_client.py` via `langchain-anthropic`), `GOOGLE_API_KEY` (used by `ui_app.py` via `langchain-google-genai`), `LANGCHAIN_TRACING_V2`, `LANGCHAIN_ENDPOINT`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`.

### Testing

| Variable | Behavior |
|---|---|
| `UPDATE_TEST_DATA` | `"1" / "true" / "True" / "yes" / "YES"` triggers snapshot rewriting in `read_json` (`tests/conftest.py:132`) |

### Environment Modes

- **Local dev (SQLite)** — leave `DB_CONNECT=local`, `uvicorn main:app --reload`. DB at `./greythr.db`.
- **Production (MySQL RDS)** — set `DB_CONNECT` to anything else, populate `DB_*`, override `SECRET_KEY`, deploy via Docker/ECS.
- **Tests** — always SQLite at `./test_db.sqlite3` regardless of `.env`.

## Companion Scripts (MCP & UI)

Three scripts layer an AI agent over the FastAPI app via MCP (stdio subprocess transport).

### `mcp_server.py` — FastAPI → MCP Bridge

```python
from main import app
from fastmcp import FastMCP

headers = {"Authorization": "Bearer <YOUR_JWT_OR_SECRET_TOKEN>"}
mcp = FastMCP.from_fastapi(
    app=app, name="Greythr clone app", httpx_client_kwargs={"headers": headers}
)
if __name__ == "__main__":
    mcp.run()
```

Imports the FastAPI `app` directly and republishes every route as an MCP tool. The Bearer header is injected into all downstream HTTP calls.

```powershell
python mcp_server.py
```

### `mcp_client.py` — Claude Agent

- LLM: `ChatAnthropic(model="claude-sonnet-4-5")`.
- Uses `MultiServerMCPClient` to spawn `mcp_server.py` as a subprocess and `client.get_tools()` to discover tools.
- LangGraph nodes: `chat_node` (Claude with bound tools) → `tools` (executes tool calls) → conditional loop.
- Demo query is hardcoded inside the script (logs in as `vishalpal0602@gmail.com / Testing` and asks for the user's full HR details).

```powershell
python mcp_client.py
```

### `ui_app.py` — Streamlit Web UI

- LLM: `ChatGoogleGenerativeAI(model="gemini-2.5-flash")`.
- Title: "GreyHR Clone MCP Chatbot".
- Caches the LangGraph chatbot via `@st.cache_resource`.
- Bridges Streamlit's sync world to the async LangGraph via a custom `run_async_in_sync()` helper.

```powershell
streamlit run ui_app.py
```

Open http://localhost:8501. Both `mcp_client.py` and `ui_app.py` start `mcp_server.py` themselves — you do **not** need to run it separately.

### Flow

```
User
  → mcp_client.py / ui_app.py (LangGraph + LLM)
    → MCP (stdio subprocess)
      → mcp_server.py (FastMCP wrapper)
        → FastAPI app (main.py)
          → SQLAlchemy / SQLite|MySQL
```

## Gotchas & Notes

### Security / Secrets

- **`.env` is committed to the repo** and contains a real RDS host (`greythr-db.ct6kewgmwlnc.ap-south-1.rds.amazonaws.com`), an Anthropic API key, a Google API key, and LangChain credentials. Treat any pushed commits as compromised; rotate keys and move to GitHub Secrets / AWS Secrets Manager before anything else.
- `SECRET_KEY` has a hardcoded default in `routers/auth.py`. Production must override.
- Login is **plain-text password comparison** (`routers/auth.py:50`). bcrypt helpers in `database/common.py` exist and are used by `insert_db_data.py`, so seeded production users will currently fail to log in until the auth flow is upgraded to verify the hash.

### Database Files in Repo

- `greythr.db` (~57 KB) and `test_db.sqlite3` (~57 KB) are checked in. They should arguably be in `.gitignore`. `test_db.sqlite3` is recreated by `conftest.py` every test session — its committed contents don't matter functionally.

### Naming / Cosmetic

- App title: `"Grethr Clone API 12345"` (`main.py:11`) — typo.
- Health response: `"Welcome to My Grehthrapp By Kishan"` — likely tested verbatim by `tests/test_cases/test_health.py`; don't change blindly.
- `common/attendance.py:170` error message: `"Employee Not Founds"`.

### Testing / Coverage

- `--cov-fail-under=100` is **strict**. Any new module not listed in `.coveragerc`'s `omit` block must be fully covered or CI fails.
- `main.py`, `database/database.py`, `database/common.py`, and MCP/UI scripts are intentionally untested.
- `tests/conftest.py:19` hardcodes the test DB path; setting `DB_CONNECT` does nothing in tests.

### Schema / Migration

- No Alembic. Schema lives only in `database/models.py`; tables are created on app startup. Any column change requires deleting `greythr.db` (or running a DB migration manually for RDS).
- Composite uniqueness (`employee+year` for Salary/Leave, `employee+month` for Payslip) is enforced only in `common/` code, not at the DB level. Concurrent writes can violate it.

### Business Logic Risk

- Leave approvals don't check balance and don't detect overlaps.
- Approval routing is locked to the manager-at-creation; later reassignments don't redirect pending requests.
- All monetary fields are `Float`.
- Manager-scope endpoints return 404 on cross-team access, masking real "not found" cases.

### CORS / Network

- CORS allows only `http://localhost:3000`. Frontend integration outside dev needs a code change in `main.py:24-30`.

### MCP Server

- `mcp_server.py` ships with a literal placeholder Bearer token (`"<YOUR_JWT_OR_SECRET_TOKEN>"`). The MCP agents won't authenticate against any non-trivial endpoint until this is replaced with a real token at runtime (or the script is updated to fetch one).
