# 🏦 FastAPI Banking System

A full-stack **Bank Account Management API** built with **FastAPI**, **MySQL**, and **Docker**, featuring JWT authentication, role-based access control, async database operations, transaction safety, load testing, GitHub Actions CI/CD, and VPS production deployment.

The project includes a **React + Vite frontend dashboard** for testing and interacting with the API.

---

# 🚀 Features

* 🔐 JWT Authentication
* 🛡️ Role-Based Access Control
* ⚡ Async FastAPI + Async SQLAlchemy
* 🐳 Dockerized Backend, Frontend & Database
* 🏦 Account Management
* 💸 Deposit, Withdraw & Transfer System
* 🧾 Transaction Ledger
* 👑 Admin Management
* ❤️ Health Monitoring Endpoint
* 🧪 Full Async Pytest Suite
* 📈 k6 Load Testing & Benchmarking
* 🌐 VPS Production Deployment
* 🔒 HTTPS + Nginx Reverse Proxy
* 🚦 Rate Limiting using SlowAPI
* 🚀 GitHub Actions CI/CD

> Demo deployment currently offline.

---

# 🌐 Live Demo

Frontend:

```text
https://bank.dhruvcore.com/
```

---

# 📸 Preview

![Login Preview](screenshots/login.gif)

---

# 🏗️ Tech Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| Backend          | FastAPI                 |
| Database         | MySQL                   |
| ORM              | SQLAlchemy 2.x Async    |
| Async Driver     | aiomysql                |
| Frontend         | React + Vite            |
| Authentication   | JWT                     |
| Password Hashing | bcrypt + passlib        |
| Authorization    | RBAC                    |
| Testing          | Pytest + pytest-asyncio |
| Load Testing     | k6                      |
| Server           | Uvicorn / Gunicorn      |
| Containerization | Docker + Docker Compose |
| Reverse Proxy    | Nginx                   |
| SSL              | Certbot + Let's Encrypt |
| CI/CD            | GitHub Actions          |

---

# 🌐 Frontend Dashboard

A frontend dashboard is included using:

* React
* Vite
* JavaScript

## Frontend Features

* Signup & Login
* Create Accounts
* Deposit Money
* Withdraw Money
* Transfer Money
* View Transaction History
* JWT Protected API Calls

> This frontend is an API interaction dashboard, not a full production banking UI.

---

# 🧠 Architecture Highlights

* Layered service architecture
* Async-first backend design
* Config-driven business rules
* Dockerized multi-service environment
* CI tested with GitHub Actions
* Nginx reverse proxy deployment
* Production-ready VPS infrastructure
* JWT + RBAC secured architecture

---

# 🧠 Core Modules

## 🔐 Authentication

* JWT-based signup/login
* Password hashing with bcrypt
* Protected routes
* RBAC authorization system

## 🏦 Account Management

* Multiple accounts per user
* Unique account numbers
* Initial balance set to 0
* Fetch all user accounts

## 🔄 Account Lifecycle

```text
ACTIVE → usable
CLOSED → blocked
```

Implements soft-close account behavior similar to real banking systems.

## 💸 Transactions

* Deposit
* Withdraw
* Transfer

## 👑 Admin Features

* View all users
* View all accounts
* Close accounts
* RBAC-protected admin routes

## ❤️ Health Monitoring

The API includes a health monitoring endpoint for deployment and infrastructure checks.

### Endpoint

```http
GET /health
```

### Purpose

* Verify API availability
* Check database connectivity
* Support Docker/container health monitoring

### Example Healthy Response

```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Application is running and database is accessible"
}
```

---

# 🛡️ Safety & Integrity

* Prevents negative balances
* Prevents self-transfer
* Allows only ACTIVE accounts
* Atomic database transactions using commit/rollback
* JWT-secured endpoints
* HTTPS encryption in production

---

# 🧾 Transaction Ledger

Every transaction is recorded for:

* Auditing
* Analytics
* Fraud detection foundations

---

# 🧠 Business Rules

* Deposit limits
* Withdraw limits
* Transfer limits
* Config-driven validation rules

---

# 📁 Project Structure

```text
fastapi-banking-system/
│
├── backend/
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── db/
│   ├── core/
│   ├── dependencies/
│   ├── tests/
│   └── main.py
│
├── docker/
│   ├── .env
│   ├── docker-compose.yml
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
├── screenshots/
├── .github/
├── .dockerignore
├── .gitignore
├── LICENSE
├── load_test.js
├── README.md
└── requirements.txt
```

---

# ⚙️ Environment Variables

## 🐳 Docker Environment

```env
COMPOSE_PROJECT_NAME=banking-app

ENV=docker

DB_USER=banking_user
DB_PASSWORD=your_password_here

MYSQL_ROOT_PASSWORD=your_root_password_here

DB_NAME=banking
TEST_DB_NAME=banking_test

ADMIN_USERNAME=your_name
ADMIN_PASSWORD=your_password

SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> `DB_HOST` and `DB_PORT` are internally handled by Docker using `banking-db:3306`.

## 💻 Local Development

```env
ENV=dev

DB_USER=banking_user
DB_PASSWORD=your_password

DB_HOST=127.0.0.1
DB_PORT=3008

DB_NAME=banking

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Testing Environment

```env
ENV=test

DB_USER=banking_user
DB_PASSWORD=your_password

DB_HOST=127.0.0.1
DB_PORT=3008

TEST_DB_NAME=banking_test

SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# ⚙️ Local Setup

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔐 Authentication

Protected routes require:

```text
Authorization: Bearer <your_token>
```

## JWT Authentication Example

```bash
curl -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

```bash
curl http://127.0.0.1:8000/api/accounts \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

# 📘 Swagger OpenAPI Notes

* Protected routes use `Authorization: Bearer <token>`.
* `/api/signup` and `/api/login` are public.
* `/api/accounts`, `/api/transfer`, `/api/transactions/{account_id}` and account operations require a valid JWT.
* Example request bodies are shown in Swagger UI under each endpoint.

---

# ✅ Acceptance Criteria

* Swagger/OpenAPI docs show JWT authentication instructions and `Authorize` support.
* Every endpoint includes a clear summary and description.
* Example request bodies are available for signup, login, account creation, deposit, withdraw, and transfer.
* Protected endpoints require a Bearer token and are grouped under `Authentication` / `Accounts` tags.
* Developer onboarding covers local startup, docs, and sample auth requests.

---

# 🌐 VPS Production Deployment

This project is deployed on a Linux VPS using Docker, Nginx, HTTPS, GitHub Actions, and a production-style reverse proxy setup.

## Infrastructure

* Hostinger VPS
* Ubuntu 24.04
* Dockerized FastAPI backend
* Dockerized React frontend
* Dockerized MySQL database
* Nginx reverse proxy
* HTTPS enabled with Certbot + Let's Encrypt
* GitHub Actions CI/CD

## Production Stack

### Backend

* FastAPI
* Async SQLAlchemy
* JWT Authentication
* RBAC authorization
* Dockerized API container

### Frontend

* React + Vite
* Dockerized frontend container
* Nginx reverse proxy integration

### Database

* MySQL 8
* Dedicated Docker container
* Persistent Docker volumes

## Production Security

* Swagger/OpenAPI disabled in production
* HTTPS enforced
* SSH key authentication
* UFW firewall configured
* JWT authentication
* bcrypt password hashing
* Nginx reverse proxy isolation
* Rate limiting using SlowAPI

## Deployment Flow

```text
git push origin main
        ↓
GitHub Actions
        ↓
SSH into VPS
        ↓
git pull
        ↓
docker compose up --build -d
```

---

# 🐳 Docker Setup

## Run Application

```bash
docker-compose up --build
```

## Reset Database

```bash
docker-compose down -v
```

## Running Tests Inside Docker

When running tests inside the `banking-api` container, Docker networking is used automatically.

The test suite switches to:

```text
banking-db:3306
```

instead of:

```text
127.0.0.1:3008
```

This allows the same test suite to work both:

* locally on the host machine
* inside Docker containers

---

# 🧪 Testing

## Run Tests

### Local Machine

```bash
$env:PYTHONPATH="."
$env:ENV="test"

python -m pytest -v
```

### Inside Docker Container

```bash
docker exec -it banking-api bash

export ENV=docker

python -m pytest -v
```

## Test Coverage Includes

* MySQL-based testing
* Per-test database reset
* Async-safe fixtures
* Dependency overrides
* JWT authentication
* RBAC authorization
* Account creation
* Deposits
* Withdrawals
* Transfers
* Transaction history
* Admin endpoints

---

# ⚙️ Async Fixes

## Critical Issues Fixed

* Fixed Windows event loop issues
* Eliminated cross-loop DB errors
* Added per-test engine isolation
* Fixed connection leaks

---

# 🚀 Performance & Load Testing

The API was stress-tested using **k6** against production-style environments:

* FastAPI running in Docker
* MySQL running in Docker
* Async SQLAlchemy + aiomysql
* JWT Authentication
* bcrypt password hashing
* Rate limiting enabled
* Mixed authenticated banking workloads

## Run Load Test

```bash
k6 run load_test.js
```

---

# 📈 Performance Results

## Windows Docker Testing

| Environment | Workers | Stable Range | Stress Range    | Overload Range |
| ----------- | ------- | ------------ | --------------- | -------------- |
| Windows     | 2       | ~200 users   | ~250–300 users  | 300+ users     |

---

# 🐧 Linux VPS Production Testing

## VPS Specifications

* 2 vCPU
* 8GB RAM
* Ubuntu 24.04
* Dockerized environment

## Tested Workflows

* Signup
* Login
* Account creation
* Deposits
* Withdrawals
* Transfers
* Transaction history
* Profile updates
* Account deletion
* Admin endpoints

## Production Results

* ~534 requests/sec observed
* 111k+ HTTP requests processed
* 55k+ iterations completed

## Stable Range

* ~100–300 realistic concurrent active users

## Stress Range

* ~300–500 concurrent virtual users

## Overload Behavior

At aggressive loads beyond 500 concurrent VUs:

* Increased latency observed
* High 429 rate limiting responses
* No catastrophic crashes
* Services remained operational

---

# 🧠 Bottleneck Analysis

| Bottleneck                   | Cause                                             |
| ---------------------------- | ------------------------------------------------- |
| bcrypt hashing               | CPU-intensive password hashing during auth flows  |
| MySQL connection pool limits | Limited database connections under concurrency    |
| Single MySQL container       | Single-node database write pressure               |
| Request queueing delays      | High concurrent traffic waiting for workers       |
| Rate limiting                | Auth-heavy traffic triggering 429 responses       |

---

# 🔧 Optimizations Applied

* Async database engine
* Connection pooling
* Rate limiting
* Docker networking fixes
* Removed SQLite fallback
* MySQL-only architecture
* HTTPS production deployment
* Nginx reverse proxy
* JWT authentication
* RBAC admin authorization
* GitHub Actions CI/CD pipeline

---

# 🏗️ Stability Summary

| Metric                          | Result                         |
| ------------------------------- | ------------------------------ |
| Requests/sec Observed           | ~534 req/s                     |
| Total HTTP Requests Processed   | 111k+                          |
| Iterations Completed            | 55k+                           |
| Maximum Concurrent VUs Survived | 500                            |
| Catastrophic Crashes            | 0                              |
| Container Stability             | Services remained operational  |

---

# 🏁 Final Status

* ✅ Fully functional backend
* ✅ Dockerized full-stack environment
* ✅ MySQL-only architecture
* ✅ HTTPS production deployment
* ✅ JWT-secured API
* ✅ RBAC admin authorization
* ✅ CI/CD operational
* ✅ VPS secured and hardened
* ✅ All tests passing
* ✅ Load tested in live VPS environment
* ✅ Stable under moderate concurrent traffic
* ✅ Survived 500 concurrent k6 virtual users without total service collapse

Stable behavior observed around ~300 concurrent users.

---

# 🚀 Future Improvements

* Add Redis caching
* Increase worker processes
* Add background task queues
* Implement load balancing
* Enable horizontal scaling
* Add observability stack with Grafana and Prometheus
* Add database replication

---

# 🎯 Capacity Summary

* ~200–300 concurrent users on Docker Desktop Windows
* ~300–500 concurrent users on Linux VPS environments

---

# 🧠 Key Learnings

* Managing async DB connections under load
* Debugging connection pool exhaustion
* Understanding infrastructure bottlenecks using k6
* Comparing Windows vs Docker vs Linux performance
* Deploying secure Dockerized applications on VPS infrastructure
* Production hardening using Nginx, HTTPS, and firewalls

---

# ⚠️ Limitations

* Single instance deployment
* No Redis caching layer
* Performance constrained by MySQL connection pool
* No horizontal scaling yet

---

# 📌 License

This project is intended for educational and portfolio purposes.
