# 🏦 FastAPI Banking System (Production-Level Backend)

A production-ready **Bank Account Management API** built with **FastAPI, MySQL, Async SQLAlchemy, and Docker**.

---

## 🚀 Project Overview

* 🔐 JWT Authentication
* 🏦 Account Management
* 💸 Transactions (Deposit, Withdraw, Transfer)
* ⚙️ Async MySQL (SQLAlchemy + aiomysql)
* 🧪 Pytest testing (MySQL-based)
* 📊 Load tested with k6
* 🐳 Dockerized (API + MySQL + Frontend)

---

## 🌐 Live Demo

* **Frontend:** https://fastapi-banking-system.vercel.app          (current no available)
* **Backend:** https://fastapi-banking-system.onrender.com         (current no available)
* **API Docs:** https://fastapi-banking-system.onrender.com/docs   (current no available)

---

## 🧠 Features

### 🔐 Authentication

* JWT-based login/signup
* Password hashing with bcrypt
* Protected routes

---

### 🏦 Account Management

* Multiple accounts per user
* Unique account numbers
* Balance initialized to 0
* Fetch all user accounts

---

### 🔄 Account Lifecycle

* ACTIVE → usable
* CLOSED → blocked
* No deletion (real-world banking logic)

---

### 💸 Transactions

* Deposit
* Withdraw
* Transfer

---

### 🛡️ Safety & Integrity

* Prevent negative balances
* Prevent self-transfer
* Only ACTIVE accounts allowed
* Atomic DB transactions (commit/rollback)

---

### 🧾 Transaction Ledger

* Every transaction recorded
* Enables auditing
* Foundation for analytics & fraud detection

---

## 🧠 Business Rules

* Deposit limits
* Withdraw limits
* Transfer limits
* Config-driven rules

---

## 🧱 Tech Stack

| Layer     | Tech               |
| --------- | ------------------ |
| Backend   | FastAPI            |
| ORM       | SQLAlchemy (Async) |
| Database  | MySQL              |
| Driver    | aiomysql           |
| Auth      | JWT                |
| Security  | bcrypt             |
| Testing   | pytest             |
| Load Test | k6                 |
| DevOps    | Docker             |

---

## 📁 Project Structure

```
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
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── .env
│   ├── .env.production
│   ├── .gitignore
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── screenshots/
│
├── .dockerignore
├── .gitattributes
├── .gitignore
├── LICENSE
├── load_test.js
├── main.sql
├── README.md
└── requirements.txt

```

---

## ⚙️ Environment Variables

```
ENV=dev

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3008
DB_NAME=bankaccountsystem

TEST_DB_NAME=bankaccountsystem_test

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Docker Setup

### Run Application

```
docker-compose up --build
```

### Reset Database

```
docker-compose down -v
```

---

## 🧪 Testing

### Run Tests

```
$env:PYTHONPATH="."
$env:ENV="test"
pytest -v
```

### Test Features

* MySQL test database (no SQLite)
* Per-test DB reset
* Async-safe fixtures
* Dependency overrides

---

## ⚙️ Async Fixes (Critical)

* Fixed Windows event loop issues
* Eliminated cross-loop DB errors
* Per-test engine isolation
* Fixed connection leaks
* Fixed password encoding (`@ → %40`)

---

## 📊 Load Testing (k6)

### Run

```
k6 run load_test.js
```

---

## 📈 Performance Results

### Windows (2 Workers)

* Stable: ~200 users
* Stress: ~250–300 users
* Overload: 300+ users

### Linux (Estimated, 4 Workers)

* Stable: ~400–500 users
* Max: ~600–700 users

---

## 🧠 Bottlenecks Identified

* Windows socket limitations
* Uvicorn worker count
* MySQL connection pool limits
* Request queueing delays

---

## 🔧 Optimizations Applied

* Async database engine
* Connection pooling
* Rate limiting
* Docker networking fixes
* Removed SQLite fallback

---

## 🏁 Final Status

* ✅ Fully functional backend
* ✅ MySQL-only architecture
* ✅ All tests passing
* ✅ Load tested up to 1000 VUs
* ✅ Performance limits identified

---

## 🚀 Future Improvements

* Migrate to Linux (WSL2 or cloud VM)
* Increase worker processes
* Add Redis caching
* Implement load balancer
* Enable horizontal scaling

---

## 🎯 Capacity Summary

* ~300 concurrent users (Windows setup)
* ~500+ users (Linux production setup)

---

## 📌 License

This project is for educational and portfolio purposes.
