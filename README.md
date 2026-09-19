# GreytHR Clone API 🏢

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://docs.astral.sh/uv/)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![AWS ECS](https://img.shields.io/badge/AWS-ECS%20Fargate-FF9900?logo=amazonaws\&logoColor=white)](https://aws.amazon.com/ecs/)
[![AWS CDK](https://img.shields.io/badge/AWS-CDK-FF9900?logo=amazonaws\&logoColor=white)](https://aws.amazon.com/cdk/)

A **GreytHR-inspired HR management REST API** built with **FastAPI, SQLAlchemy and Pydantic**.

The application provides role-based APIs for **Admin, Manager and User** workflows including employee management, attendance, leave management, payroll, expense claims and attendance regularization.

The project is containerized with Docker and deployed to **AWS ECS Fargate**, with infrastructure managed using **AWS CDK** and deployments automated through **GitHub Actions**.

> **Built by Vishal Kumar Pal**

---

## ✨ Features

* 👥 Employee management
* 🏛️ Department and role management
* ⏰ Attendance tracking
* 📝 Leave allocation and approval
* 💰 Salary and payslip management
* 🧾 Expense claims
* 🔄 Attendance regularization
* 🔐 JWT-based authentication
* 👑 Admin / Manager / User access control
* 🗄️ SQLAlchemy ORM
* 🔄 Alembic database migrations
* 🐳 Multi-stage Docker build
* ☁️ AWS ECS Fargate deployment
* 🏗️ AWS CDK infrastructure
* 📈 ECS Auto Scaling
* 🔍 Trivy container security scanning
* ⚙️ GitHub Actions CI/CD

---

## 🛠️ Tech Stack

| Layer                  | Technology                |
| ---------------------- | ------------------------- |
| API                    | FastAPI                   |
| Server                 | Uvicorn                   |
| ORM                    | SQLAlchemy                |
| Validation             | Pydantic                  |
| Authentication         | JWT                       |
| Database Migration     | Alembic                   |
| Local Database         | SQLite                    |
| Testing                | pytest + pytest-cov       |
| Formatting             | Black                     |
| Linting                | Ruff                      |
| Package Manager        | uv                        |
| Dependency Definition  | pyproject.toml            |
| Dependency Lock        | uv.lock                   |
| Containerization       | Docker                    |
| Container Registry     | Amazon ECR                |
| Compute                | Amazon ECS Fargate        |
| Load Balancer          | Application Load Balancer |
| Infrastructure as Code | AWS CDK (Python)          |
| Monitoring             | Amazon CloudWatch         |
| Security Scanning      | Trivy + ECR Image Scan    |
| CI/CD                  | GitHub Actions            |
| Python                 | 3.12                      |

---

## 🏗️ Architecture

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/5036478e-a96a-4da9-8071-0b44b94a3ec9" />

The application runs as Docker containers on **ECS Fargate** inside private subnets.

Public traffic reaches the application through an **Application Load Balancer**. ECS tasks are not directly exposed to the internet.

Infrastructure provisioning and application deployment are intentionally separated:

```text
AWS CDK
   ↓
Base AWS Infrastructure

GitHub Actions
   ↓
Build + Test + Docker + ECS Deployment
```

---

## 📁 Project Structure

```text
greythr-clone-app-api/
│
├── main.py                     # FastAPI application entry point
├── pyproject.toml              # Dependencies and tool configuration
├── uv.lock                     # Locked Python dependencies
├── .python-version             # Python version
│
├── common/                     # Business logic
├── database/                   # Database configuration and ORM models
├── routers/                    # API routers
├── schema/                     # Pydantic schemas
├── utils/                      # Shared utilities
│
├── alembic/                    # Database migrations
│
├── tests/                      # Automated tests
│
├── infra/                      # AWS CDK infrastructure
│   ├── app.py                  # CDK application entry point
│   ├── config/
│   └── infra/
│       ├── network_stack.py
│       ├── security_stack.py
│       ├── ecr_stack.py
│       ├── iam_stack.py
│       ├── ecs_stack.py
│       └── alb_stack.py
│
├── .github/
│   └── workflows/
│       └── cicd.yaml           # CI/CD pipeline
│
├── Dockerfile
└── .dockerignore
```

---

## 🧩 Application Design

The backend follows a simple layered structure:

```text
Request
   ↓
Router
   ↓
Business Logic
   ↓
SQLAlchemy
   ↓
Database
```

### Layers

**Routers** handle HTTP requests, authentication, dependency injection and role-based access.

**Common** contains reusable business logic and CRUD operations.

**Database** manages SQLAlchemy sessions and ORM models.

**Schema** contains Pydantic request and response models.

---

## 👥 Role-Based Access

| API          | Role    | Access                       |
| ------------ | ------- | ---------------------------- |
| `/admin/*`   | Admin   | Organization-wide access     |
| `/manager/*` | Manager | Direct-report related access |
| `/user/*`    | User    | Own records                  |

---

## 🔐 Authentication

Authentication uses **JWT Bearer tokens**.

Login endpoints:

```text
POST /auth/token
POST /auth/login_json
```

Authenticated requests use:

```http
Authorization: Bearer <token>
```

Example token response:

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

---

## 📡 Main API Areas

### Admin

Admin APIs provide organization-level management for:

* Employees
* Departments
* Roles
* Attendance
* Leave allocations
* Leave applications
* Regularizations
* Expense claims
* Salaries
* Payslips

### Manager

Manager APIs provide access to:

* Subordinates
* Attendance
* Leave applications
* Regularizations
* Expense claims

### User

Users can manage or view their own:

* Profile
* Attendance
* Leave
* Leave applications
* Regularizations
* Expense claims
* Salary
* Payslips
* Roles
* Departments

For complete request and response schemas, use Swagger:

```text
http://localhost:8000/docs
```

---

## ⚙️ Local Setup

### Prerequisites

Install:

* Python 3.12
* Git
* uv

Clone the repository:

```bash
git clone https://github.com/vishalpal-06/greythr-clone-app-api.git
cd greythr-clone-app-api
```

Install the locked dependencies:

```bash
uv sync
```

`uv` creates and manages the project virtual environment automatically.

---

## ▶️ Run Locally

Start the FastAPI application:

```bash
uv run uvicorn main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Health endpoint:

```text
GET /
```

---

## 📦 Dependency Management

Application dependencies are managed using:

```text
pyproject.toml
        +
     uv.lock
```

Install dependencies:

```bash
uv sync
```

Add a dependency:

```bash
uv add <package>
```

Add a development dependency:

```bash
uv add --dev <package>
```

Remove a dependency:

```bash
uv remove <package>
```

Run commands inside the project environment:

```bash
uv run <command>
```

The application does **not** use a root `requirements.txt`.

---

## 🗄️ Database Migrations

Database schema changes are managed using **Alembic**.

Create a migration:

```bash
uv run alembic revision --autogenerate -m "migration description"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

View migration history:

```bash
uv run alembic history
```

Rollback one migration:

```bash
uv run alembic downgrade -1
```

Alembic configuration is maintained through `pyproject.toml`.

---

## 🧪 Testing

Run all tests:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=.
```

CI requires **100% test coverage**:

```bash
uv run pytest \
  --disable-warnings \
  --maxfail=1 \
  --cov=. \
  --cov-fail-under=100
```

---

## 🧹 Code Quality

### Black

Check formatting:

```bash
uv run black --check .
```

Format code:

```bash
uv run black .
```

### Ruff

Run linting:

```bash
uv run ruff check .
```

Auto-fix supported issues:

```bash
uv run ruff check . --fix
```

Black, Ruff, pytest and coverage configuration are stored in `pyproject.toml`.

---

## 🐳 Docker

The project uses a **multi-stage Docker build**.

The builder stage uses `uv` and the locked dependencies from:

```text
pyproject.toml
uv.lock
```

Only production dependencies are installed into the final image.

Build:

```bash
docker build -t greythr-api .
```

Run:

```bash
docker run -p 8000:8000 greythr-api
```

Open:

```text
http://localhost:8000/docs
```

The runtime container runs as a **non-root user**.

---

## ☁️ AWS Infrastructure

AWS infrastructure is defined using **AWS CDK with Python** under:

```text
infra/
```

The CDK application manages the long-lived AWS resources required by the application.

Main stacks:

```text
NetworkStack
SecurityStack
EcrStack
IamStack
EcsStack
AlbStack
```

The **ECS Task Definition and ECS Service are managed by the CI/CD pipeline**, allowing application deployments to happen independently from base infrastructure changes.

### Deploy Infrastructure Manually

```bash
cd infra
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install CDK Python dependencies:

```bash
uv pip install -r requirements.txt
```

> `infra/requirements.txt` is only for the standalone CDK project. Application dependencies are managed through the root `pyproject.toml` and `uv.lock`.

Synthesize CloudFormation:

```bash
cdk synth
```

Review changes:

```bash
cdk diff
```

Deploy:

```bash
cdk deploy --all
```

For a new AWS account/region:

```bash
cdk bootstrap
```

---

## 🚀 CI/CD

GitHub Actions automatically deploys changes pushed to `main`.

```text
Push to main
      ↓
Detect Infrastructure Changes
      ↓
Black Formatting Check
      ↓
pytest + 100% Coverage
      ↓
Build Docker Image
      ↓
Trivy Security Scan
      ↓
Push Image to Amazon ECR
      ↓
Generate ECS Task Definition
      ↓
Register Task Definition
      ↓
Create / Update ECS Service
      ↓
Configure Auto Scaling
      ↓
Wait for Stable Deployment
```

### Infrastructure Changes

Changes under:

```text
infra/**
```

trigger the CDK deployment job.

The pipeline runs:

```text
cdk synth
      ↓
cdk deploy --all
```

Application deployment continues after the required infrastructure is available.

---

## 🔍 Container Security

Before an image is pushed to ECR, CI scans it using **Trivy**.

The deployment fails when fixable:

```text
HIGH
CRITICAL
```

vulnerabilities are detected.

ECR also has image scanning enabled when images are pushed.

---

## 🚢 ECS Deployment

Each successful deployment creates a Docker image tagged with the Git commit SHA:

```text
greythr-api:<git-sha>
```

The pipeline then dynamically generates and registers a new ECS Task Definition revision.

Current task configuration:

```text
CPU       : 512
Memory    : 1024 MB
Port      : 8000
Launch    : Fargate
Network   : awsvpc
Public IP : Disabled
```

ECS tasks run in **private subnets** and receive application traffic only through the Application Load Balancer.

---

## 📈 Auto Scaling

The ECS service is configured with:

```text
Minimum Tasks : 2
Maximum Tasks : 10
```

CPU scaling target:

```text
70%
```

Memory scaling target:

```text
75%
```

Scale-in and scale-out cooldown:

```text
60 seconds
```

The deployment starts with a desired task count of `3`.

---

## 🔄 Deployment Strategy

ECS uses a rolling deployment configuration:

```text
minimumHealthyPercent = 100
maximumPercent        = 200
```

During deployment, ECS can start new tasks while keeping the existing healthy tasks available.

Deployment Circuit Breaker is enabled with automatic rollback:

```text
Deployment fails
       ↓
Circuit Breaker
       ↓
Rollback
       ↓
Previous healthy deployment
```

The pipeline waits until the ECS service becomes stable before marking deployment successful.

---

## 📊 Monitoring & Logs

ECS Container Insights is enabled.

Application container logs are sent to:

```text
/ecs/greythr-api
```

The CloudWatch log group is retained for one month.

The deployment pipeline also waits for ECS service stability and prints the final:

* Service name
* Desired tasks
* Running tasks
* Pending tasks
* Task Definition revision

---

## 🔒 Security

The deployment follows these basic security controls:

* ECS tasks run inside private subnets
* ECS tasks do not receive public IP addresses
* Internet traffic enters through the ALB
* ECS port `8000` accepts traffic only from the ALB security group
* Containers run as a non-root Linux user
* IAM execution and application task roles are separated
* Docker images are scanned before deployment
* ECR image scanning is enabled
* Production Docker builds exclude development dependencies
* AWS credentials are stored in GitHub Secrets

---

## 🔑 Required GitHub Secrets

The current pipeline requires:

| Secret                  | Purpose                              |
| ----------------------- | ------------------------------------ |
| `AWS_ACCESS_KEY_ID`     | Authenticate GitHub Actions with AWS |
| `AWS_SECRET_ACCESS_KEY` | Authenticate GitHub Actions with AWS |

Deployment configuration such as AWS region, ECR repository, ECS cluster and ECS service names is currently defined in the workflow environment.

---

## 🌐 Deployment Flow

```text
Developer
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Tests + Security Scan
    ↓
Docker Image
    ↓
Amazon ECR
    ↓
ECS Task Definition
    ↓
ECS Service
    ↓
Fargate Tasks
    ↑
Application Load Balancer
    ↑
Internet
```

---

## 👨‍💻 Author

**Vishal Kumar Pal**

GreytHR Clone API

<div align="center">

⭐ If you find this project useful, consider giving it a star!

</div>
