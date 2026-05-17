# 🏦 FastAPI Banking System

### Production-Style Banking API with FastAPI, MySQL & Docker

A production-ready **Bank Account Management API** built using **FastAPI, MySQL, Async SQLAlchemy, and Docker**.

---

# 🚀 Project Overview

- 🔐 JWT Authentication
- 🏦 Account Management
- 💸 Transactions (Deposit, Withdraw, Transfer)
- ⚙️ Async MySQL using SQLAlchemy + aiomysql
- 🧪 Pytest Testing
- 📊 Load Testing with k6
- 🐳 Dockerized Full Stack Setup

> Demo deployment currently offline.

---

# 🌐 Live Demo

- Frontend: https://vaultx.dhruvsystems.tech/
- Backend: https://fastapi-banking-system.onrender.com
- API Docs: https://fastapi-banking-system.onrender.com/docs

---

# 📸 Preview

![Login Preview](screenshots/login.gif)

---

# 🧩 Architecture Highlights

- Layered service architecture
- Async-first backend design
- Config-driven business rules
- Dockerized multi-service environment
- CI tested with GitHub Actions

---

# 🧠 Features

## 🔐 Authentication

- JWT-based signup/login
- Password hashing with bcrypt
- Protected routes

---

## 🏦 Account Management

- Multiple accounts per user
- Unique account numbers
- Initial balance set to 0
- Fetch all user accounts

---

## 🔄 Account Lifecycle

- ACTIVE → usable
- CLOSED → blocked

Implements soft-close account behavior similar to real banking systems.

---

## 💸 Transactions

- Deposit
- Withdraw
- Transfer

---

## ❤️ Health Monitoring

The API includes a health monitoring endpoint for deployment and infrastructure checks.

### Endpoint

```http
GET /health
```

### Purpose

- Verify API availability
- Check database connectivity
- Support Docker/container health monitoring

### Example Healthy Response

```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Application is running and database is accessible"
}
```

---

## 🛡️ Safety & Integrity

- Prevents negative balances
- Prevents self-transfer
- Allows only ACTIVE accounts
- Atomic database transactions using commit/rollback

---

## 🧾 Transaction Ledger

Every transaction is recorded for:

- Auditing
- Analytics
- Fraud detection foundations

---

# 🧠 Business Rules

- Deposit limits
- Withdraw limits
- Transfer limits
- Config-driven validation rules

---

# 🧱 Tech Stack

| Layer | Technology |
|------|------|
| Backend | FastAPI |
| ORM | SQLAlchemy (Async) |
| Database | MySQL |
| Driver | aiomysql |
| Authentication | JWT |
| Security | bcrypt |
| Testing | pytest |
| Load Testing | k6 |
| DevOps | Docker |

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

## 🐳 Docker Environment (Recommended)

```env
COMPOSE_PROJECT_NAME=banking-app

ENV=docker

DB_USER=banking_user
DB_PASSWORD=your_password_here

MYSQL_ROOT_PASSWORD=your_root_password_here

DB_NAME=banking
TEST_DB_NAME=banking_test

SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Note: `DB_HOST` and `DB_PORT` are internally handled by Docker (`banking-db:3306`).

---

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

---

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

### 🐳 Running Tests Inside Docker

When running tests inside the `banking-api` container,
Docker networking is used automatically.

The test suite switches to:

```text
banking-db:3306
```

instead of:

```text
127.0.0.1:3008
```

This allows the same test suite to work both:
- locally on the host machine
- inside Docker containers

---

## 🚀 Developer Quick Start

1. Create a `.env` file with the environment variables above.
2. Start the backend with:

```bash
uvicorn backend.main:app --reload --port 8000
```

3. Open the interactive OpenAPI docs at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

4. Use `/api/login` to sign in and then click the `Authorize` button.

---

## 📘 Swagger OpenAPI Notes

- Protected routes use `Authorization: Bearer <token>`.
- `/api/signup` and `/api/login` are public.
- `/api/accounts`, `/api/transfer`, `/api/transactions/{account_id}` and account operations require a valid JWT.
- Example request bodies are shown in Swagger UI under each endpoint.

### JWT Authentication Example

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

## ✅ Acceptance Criteria

- Swagger/OpenAPI docs show JWT authentication instructions and `Authorize` support.
- Every endpoint includes a clear summary and description.
- Example request bodies are available for signup, login, account creation, deposit, withdraw, and transfer.
- Protected endpoints require a Bearer token and are grouped under `Authentication` / `Accounts` tags.
- Developer onboarding covers local startup, docs, and sample auth requests.

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

---

## Test Features

- MySQL-based testing
- Per-test database reset
- Async-safe fixtures
- Dependency overrides

---

# ⚙️ Async Fixes

## Critical Issues Fixed

- Fixed Windows event loop issues
- Eliminated cross-loop DB errors
- Added per-test engine isolation
- Fixed connection leaks

---

# 📊 Load Testing (k6)

## Run Load Test

```bash
k6 run load_test.js
```

---

# 📈 Performance Results

## Windows (2 Workers)

- Stable: ~200 users
- Stress: ~250–300 users
- Overload: 300+ users

---

## Linux (Estimated)

Based on benchmarks:

- ~300–500 concurrent users expected

> Actual performance depends on hardware and deployment setup.

---

# 🧠 Bottlenecks Identified

- Windows socket limitations
- Uvicorn worker count
- MySQL connection pool limits
- Request queueing delays

---

# 🔧 Optimizations Applied

- Async database engine
- Connection pooling
- Rate limiting
- Docker networking fixes
- Removed SQLite fallback

---

# 🏁 Final Status

- ✅ Fully functional backend
- ✅ MySQL-only architecture
- ✅ All tests passing
- ✅ CI pipeline passing
- ✅ Dockerized full-stack environment
- ✅ Load tested up to 1000 virtual users

Stable behavior observed around ~300 concurrent users.

---

# 🚀 Future Improvements

- Migrate to Linux (WSL2 or cloud VM)
- Increase worker processes
- Add Redis caching
- Implement load balancing
- Enable horizontal scaling

---

# 🎯 Capacity Summary

- ~200–300 concurrent users on Docker Desktop (Windows)
- ~300–500 expected on native Linux environments

---

# 🧠 Key Learnings

- Managing async DB connections under load
- Debugging connection pool exhaustion
- Understanding infrastructure bottlenecks using k6
- Comparing Windows vs Docker vs Linux performance

---

# ⚠️ Limitations

- Single instance deployment
- No Redis caching layer
- Performance constrained by MySQL connection pool

---

# 📌 License

This project is intended for educational and portfolio purposes.
