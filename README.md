# GitHub README.md for GreytHR Clone API

Here's the extracted and reformatted content for your README.md:

```markdown
# GreytHR Clone API 🏢

A Greythr/greytHR HR-platform clone exposed as a **FastAPI** service backed by 
**SQLAlchemy** and validated through **Pydantic**. Covers core HR operations with 
role-scoped API surfaces authenticated via JWT bearer tokens.

> Built by **Vishal Kumar Pal**

---

## 🚀 Live Demo & Docs

- **API Base**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **Health Check**: `GET /` → `{"status": "Welcome to My Grehthrapp By Vishal Kumar Pal"}`
- **Streamlit UI**: `http://localhost:8501`

---

## ✨ Features

- 👥 **Employee Management** — Full CRUD with role & department associations
- 🏛️ **Department & Role Management** — Admin-controlled organizational structure
- ⏰ **Attendance Tracking** — Punch-in system with date-based queries
- 📝 **Leave Management** — Allocation + applications with approval workflows
- 💰 **Payroll** — Salary records + payslip generation
- 🧾 **Expense Claims** — Submission and approval system
- 🔄 **Regularization** — Attendance correction request workflows
- 🤖 **AI Agent Integration** — MCP + Claude/Gemini chatbot over the same API
- 🔐 **JWT Authentication** — Role-scoped endpoints (Admin / Manager / User)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI 0.124.0 |
| **Server** | Uvicorn 0.38.0 |
| **ORM** | SQLAlchemy 2.0.27 |
| **Dev DB** | SQLite (built-in) |
| **Prod DB** | MySQL (PyMySQL) |
| **Validation** | Pydantic 2.11.7 |
| **Auth** | PyJWT 2.10.1 (HS256) |
| **Password Hashing** | bcrypt 5.0.0 via passlib |
| **Testing** | pytest 9.0.2 + pytest-cov 7.0.0 |
| **Formatting** | black 25.11.0 |
| **AI/LLM** | LangChain + LangGraph |
| **MCP** | fastmcp 2.13.3 |
| **UI** | Streamlit |
| **Deployment** | Docker + AWS ECS (Fargate) |
| **CI/CD** | GitHub Actions |
| **Python** | 3.12 |

---

## 📁 Project Structure

```
greythr-clone-app-api/
├── main.py                    # FastAPI app entry point
├── mcp_server.py              # FastMCP wrapper (FastAPI → MCP tools)
├── mcp_client.py              # Claude agent (LangGraph over MCP)
├── ui_app.py                  # Streamlit chatbot (Gemini 2.5 Flash)
├── insert_db_data.py          # Production RDS seeder
│
├── routers/
│   ├── auth.py                # JWT login endpoints
│   ├── admin/                 # /admin/* (10 sub-routers)
│   ├── manager/               # /manager/* (6 sub-routers)
│   └── user/                  # /user/* (10 sub-routers)
│
├── database/
│   ├── database.py            # Engine setup & session
│   ├── models.py              # SQLAlchemy ORM models
│   └── common.py              # bcrypt helpers
│
├── schema/                    # Pydantic v2 schemas
├── common/                    # Business logic layer
│
├── tests/
│   ├── conftest.py            # Fixtures & test DB setup
│   ├── seed_db.py             # JSON-based test data seeder
│   ├── test_data/             # *.json seed fixtures
│   ├── expected_responses/    # Snapshot JSONs
│   └── test_cases/            # ~31 test files
│
├── .github/workflows/ci.yaml  # CI/CD pipeline
├── Dockerfile
├── ecs-task-def.json
└── requirements.txt
```

---

## 🏗️ Architecture

```
┌─────────────┐    ┌──────────────┐    ┌──────────────────┐
│   Routers   │───▶│   Common     │───▶│    Database      │
│  (HTTP +    │    │  (Business   │    │  (SQLAlchemy     │
│   Auth DI)  │    │   Logic)     │    │   Models)        │
└─────────────┘    └──────────────┘    └──────────────────┘
```

**Three-layer design:**
1. **Routers** — HTTP concerns, dependency injection, role-based routing
2. **Common** — Authorization, CRUD orchestration, computed fields
3. **Database** — SQLAlchemy engine, session, and ORM models

### Role-Based API Surfaces

| Mount | Role | Access Scope |
|-------|------|-------------|
| `/admin` | Admin (`is_admin=True`) | All records across all employees |
| `/manager` | Manager (any auth user) | Direct reports only |
| `/user` | User (any auth user) | Own records only (`/user/my/*`) |

---

## 🔐 Authentication

- **Type**: JWT Bearer Token (HS256)
- **TTL**: 60 minutes
- **Login Endpoints**:
  - `POST /auth/token` — Form data (Swagger-compatible)
  - `POST /auth/login_json` — JSON body (`username`, `password`)

```json
// Response
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Token Payload:**
```json
{
  "email": "user@example.com",
  "emp_id": 1,
  "is_admin": false,
  "exp": "<timestamp>"
}
```

---

## 📡 API Endpoints

<details>
<summary><b>👑 Admin Endpoints</b></summary>

| Resource | Methods |
|----------|---------|
| `/admin/employees` | GET, POST, PUT, DELETE (by id & email) |
| `/admin/roles` | POST, PUT, DELETE (by id & name) |
| `/admin/departments` | POST, PUT, DELETE (by id & name) |
| `/admin/attendance` | GET (all, by date, by employee) |
| `/admin/leaves` | GET, POST, DELETE |
| `/admin/leave-applications` | GET, PUT (status update) |
| `/admin/regularizations` | GET, PUT (status update) |
| `/admin/expense-claims` | GET, PUT (status update) |
| `/admin/payslips` | GET, POST, DELETE |
| `/admin/salaries` | GET, POST, DELETE |

</details>

<details>
<summary><b>👔 Manager Endpoints</b></summary>

| Resource | Methods |
|----------|---------|
| `/manager/subordinates` | GET (by id & email) |
| `/manager/attendance` | GET (by date, by employee) |
| `/manager/leaves` | GET |
| `/manager/leave-applications` | GET, PUT (status update) |
| `/manager/regularizations` | GET (pending, by id, by employee), PUT (status) |
| `/manager/expense-claims` | GET, PUT (status update) |

</details>

<details>
<summary><b>👤 User Endpoints</b></summary>

| Resource | Methods |
|----------|---------|
| `/user/my` | GET (profile) |
| `/user/my/attendance` | GET, POST (punch-in) |
| `/user/my/leave` | GET |
| `/user/my/leave-applications` | GET, POST, DELETE (Pending only) |
| `/user/my/regularizations` | GET, POST |
| `/user/my/expense-claims` | GET, POST, DELETE (Pending only) |
| `/user/my/payslips` | GET |
| `/user/my/salary` | GET |
| `/user/my/roles` | GET (read-only) |
| `/user/my/departments` | GET (read-only) |

</details>

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.12
- Git

### 1. Clone & Setup

```powershell
git clone <repo-url>
cd greythr-clone-app-api

# Activate virtual environment
.\venv\Scripts\Activate.ps1       # Windows
source venv/bin/activate           # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env   # create from example
```

Edit `.env`:

```env
# Database (leave as "local" for SQLite dev)
DB_CONNECT=local

# For MySQL/Production
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
DB_NAME=your_db_name

# Auth (MUST override in production)
SECRET_KEY=your-secure-secret-key
ALGORITHM=HS256

# LLM Keys (only needed for MCP/UI features)
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

### 3. Run the API

```powershell
uvicorn main:app --reload
```

> Tables are auto-created on startup. No migration step needed.

### 4. Seed the Database (Optional)

```powershell
python insert_db_data.py
```

---

## 🧪 Testing

### Run Tests

```powershell
# Full suite
pytest

# Verbose
pytest -v

# Single file
pytest tests\test_cases\test_health.py

# Filter by name
pytest -k "department" -v

# With coverage
pytest --cov=. --cov-report=html

# CI mode (strict 100% coverage)
pytest --disable-warnings --maxfail=1 --cov=. --cov-fail-under=100
```

### View Coverage Report

```powershell
start htmlcov\index.html    # Windows
open htmlcov/index.html     # Mac
```

### Update Snapshots

```powershell
$env:UPDATE_TEST_DATA = "1"
pytest tests\test_cases\test_admin_api\test_admin_department_api.py
Remove-Item Env:UPDATE_TEST_DATA
```

### Simulate CI Locally

```powershell
black --check .
pytest --disable-warnings --maxfail=1 --cov=. --cov-fail-under=100
```

> ⚠️ CI enforces **100% coverage**. New code must be fully covered or add to `.coveragerc` omit list.

---

## 🤖 AI Agent Integration

Three companion scripts layer an AI agent over the FastAPI app:

```
User
  → mcp_client.py / ui_app.py  (LangGraph + LLM)
    → MCP (stdio subprocess)
      → mcp_server.py (FastMCP)
        → FastAPI app
          → SQLAlchemy / DB
```

### MCP Server
```powershell
python mcp_server.py
```
Exposes every FastAPI route as an MCP tool.

### Claude Agent (Terminal)
```powershell
python mcp_client.py
```
LangGraph agent using `claude-sonnet-4-5`.

### Streamlit Web UI
```powershell
streamlit run ui_app.py
# Open http://localhost:8501
```
Chatbot powered by `gemini-2.5-flash`.

> Both `mcp_client.py` and `ui_app.py` start `mcp_server.py` automatically.

---

## 🐳 Docker

```powershell
# Build
docker build -t greythr-clone-api:latest .

# Run
docker run -p 8000:8000 greythr-clone-api:latest
```

---

## 🚀 CI/CD Pipeline

GitHub Actions (`.github/workflows/ci.yaml`) on push/PR to `main`:

```
Format Check (black)
    ↓
Tests (pytest 100% coverage)
    ↓
Push to AWS ECR
    ↓
Deploy to AWS ECS (Fargate)
```

**Required GitHub Secrets:**

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials |
| `AWS_REGION` | Target region |
| `ECR_REPOSITORY` | ECR repo name |
| `ECS_SERVICE_NAME` | ECS service |
| `ECS_CLUSTER_NAME` | ECS cluster |
| `ECS_CONTAINER_NAME` | Container name |

---

## 🗄️ Data Models

| Model | Key Fields |
|-------|-----------|
| `Employee` | id, name, email, password, isadmin, dept, role, manager |
| `Department` | id, name (unique) |
| `Role` | id, name (unique) |
| `Attendance` | id, punch_time, employee_id |
| `Leave` | id, year, casual/plan/probation/sick/balance counts |
| `LeaveApplication` | id, from_date, end_date, total_days, status, manager_id |
| `Regularization` | id, start_time, end_time, reason, status, manager_id |
| `Salary` | id, lpa (Float), year, employee_id |
| `Payslip` | id, basic, hra, allowances, month (1st of month), employee_id |
| `ExpenseClaim` | id, date, amount, description, status, manager_id |

---

## ⚠️ Known Limitations

| Issue | Severity |
|-------|---------|
| No leave-balance check on approval | 🔴 High |
| No overlap detection on approved leaves | 🔴 High |
| Password stored/compared as plain text | 🔴 High |
| All monetary fields use `Float` (not `Decimal`) | 🟡 Medium |
| No database migrations (Alembic) | 🟡 Medium |
| Manager reassignment doesn't reroute pending approvals | 🟡 Medium |
| No soft delete / audit trail | 🟡 Medium |
| Synchronous SQLAlchemy blocks async event loop | 🟡 Medium |
| CORS allows only `http://localhost:3000` | 🟡 Medium |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Vishal Kumar Pal** — GreytHR Clone API

---

*Generated with Claude Code* 🤖
```

---

## 💡 Tips for Your README

| Section | Action |
|---------|--------|
| Add **badges** | shields.io for build status, coverage, Python version |
| Add **screenshots** | Swagger UI, Streamlit UI screenshots |
| Add **contributing guide** | `CONTRIBUTING.md` link |
| Remove known limitations | Or move to `ISSUES.md` if public repo |
| Add `.env.example` | So users know what vars to set |



```
pytest --disable-warnings
pytest --cov=.
coverage html
```

## 🎥 MCP Demo Video
<a href="https://youtu.be/mjdOBh3INZs" target="_blank">
  <img src="https://img.youtube.com/vi/mjdOBh3INZs/0.jpg" width="100%" />
</a>

