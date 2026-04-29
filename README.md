# 🏦 FastAPI Banking System

A production-style **Bank Account Management API** built with **FastAPI**, **SQLAlchemy**, and **MySQL**.

Designed to simulate real-world fintech backend systems with **secure authentication, transactional integrity, and rule-based financial operations**.

---

## 🖼️ UI Preview

![Login](screenshots/login.gif)
Watch Full Demo:- https://youtu.be/iex0donzgtE

---

## 🌐 Live Demo

* Frontend: https://fastapi-banking-system.vercel.app
* Backend API: https://fastapi-banking-system.onrender.com
* API Docs: https://fastapi-banking-system.onrender.com/docs

---

# 🚀 Key Features

## 🔐 Authentication

* JWT-based authentication
* Secure password hashing (bcrypt)
* Case-insensitive username handling
* Protected routes using dependency injection

---

## 🏦 Account Management

* Create multiple accounts per user
* Unique account number enforcement
* Accounts initialized with **zero balance (system-controlled)**
* Fetch all user accounts securely

---

## 🔄 Account Lifecycle (NEW)

Accounts are not physically deleted. Instead, they are marked as:

* `ACTIVE` → usable account
* `CLOSED` → hidden from UI and blocked from operations

This ensures:

* Data integrity
* Transaction history preservation
* Real-world banking behavior

---

## 💸 Transactions (Core System)

### ✔ Supported Operations

* Deposit funds
* Withdraw funds with balance validation
* Transfer money between accounts

### ✔ Safety & Integrity

* Prevent overdraft (no negative balance)
* Prevent self-transfers
* Only ACTIVE accounts can perform operations
* Atomic database transactions using commit/rollback

---

## 🧠 Business Rules & Financial Constraints

### 💰 Transaction Limits

* Deposit limit per transaction
* Withdraw limit per transaction
* Transfer limit enforcement

> Limits are centrally managed via a **config module**, making the system flexible and maintainable.

---

### 🧾 Transaction Ledger

* Every operation (deposit, withdraw, transfer) is recorded
* Enables audit tracking and system transparency
* Foundation for future features like:

  * Statements
  * Analytics
  * Fraud detection

---

## 🧠 Validation Strategy

* Strong input validation using Pydantic schemas
* Backend-driven validation (never trusting frontend)
* Ownership-based authorization
* Clean separation of validation and business logic:

  * **Data validation (schemas)**
  * **Business logic (routes/services)**

---

# 🧱 Tech Stack

| Layer      | Technology             |
| ---------- | ---------------------- |
| Backend    | FastAPI                |
| ORM        | SQLAlchemy             |
| Database   | MySQL                  |
| Validation | Pydantic               |
| Auth       | JWT (python-jose)      |
| Security   | Passlib (bcrypt)       |
| Config     | python-dotenv          |
| DevOps     | Docker, Docker Compose |

---

# 📁 Project Structure

```
fastapi-banking-system/
│
├── app/
│   ├── routes/        # API endpoints    
│       (auth, accounts, transactions)
│   ├── models/        # Database models
│   ├── schemas/       # Request/response validation
│   ├── db/            # DB connection setup
│   ├── core/          # Security, config (JWT, hashing, limits)
│   └── dependencies/  # Auth middleware
│
├── main.py
├── requirements.txt
├── .env
└── .gitignore
```

---

# ⚙️ Setup Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Dhruv-Cmds/fastapi-banking-system.git
cd fastapi-banking-system
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

### Activate:

**Windows**

```bash
.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment

Create a `.env` file:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=bankaccountsystem

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=your_time
```

---

## 5️⃣ Run Server

```bash
uvicorn main:app --reload (backend)
npm run dev (frontend)
```

---

# 🐳 Docker Setup (Recommended)

Run the entire project using Docker (Backend + Frontend + MySQL).

---

## ⚙️ Requirements

* Docker
* Docker Compose

---

## 🚀 Run with Docker

```bash
docker-compose up --build
```

---

## 🌐 Services

* Backend API → http://localhost:8000
* API Docs → http://localhost:8000/docs
* Frontend → http://localhost:5173
* MySQL → localhost:3008

---

## 🔐 Environment Variables

Make sure `.env` file is configured:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=bankaccountsystem

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 🧠 Docker Notes

* Uses **named volume (`db_data`)** for MySQL persistence
* Avoids local bind mount issues (prevents DB corruption)
* Data persists across container restarts

### Reset database if needed:

```bash
docker-compose down -v
```

---

# 📌 API Endpoints

## 🔐 Auth

* `POST /signup`
* `POST /login`

## 🏦 Accounts

* `POST /accounts`
* `GET  /accounts`
* `DELETE /accounts/{id} → closes account`

## 💰 Transactions

* `POST /accounts/{id}/deposit`
* `POST /accounts/{id}/withdraw`
* `POST /transfer`

---

# 🧠 System Behavior

* Tables auto-created at startup:

```python
Base.metadata.create_all(bind=engine)
```

* Account lifecycle:

```
Create account → balance = 0  
Deposit → increases balance  
Withdraw → decreases balance  
Transfer → moves funds safely 
Close account → status = CLOSED (not deleted) 
```

---

# 🔐 Security Highlights

* JWT authentication
* Password hashing (bcrypt)
* Environment-based secrets
* Ownership-based authorization checks
* Safe transaction handling using DB locks
* Protection against race conditions

---

# 💎 Highlights

* Clean, modular architecture
* Real-world banking logic implementation
* Soft-delete system (account lifecycle)
* Transaction safety (race-condition prevention)
* Rule-based financial system (limits + validation)
* Scalable backend design
* Dockerized full-stack setup (API + Frontend + Database)
* Persistent MySQL storage using Docker volumes
* Resolved real-world DB corruption & container restart issues

---

# 🏁 Conclusion

This project demonstrates how to build a **real-world backend system** with:

* Authentication & authorization
* Database design & ORM usage
* Transaction safety & concurrency handling
* Business rule enforcement
* Clean architecture & scalability
* Containerized deployment using Docker

It serves as a strong foundation for evolving into a **full fintech platform** 🚀

---

# ⭐ Author

**Dhruv**
Backend-focused developer building systems with strong fundamentals in **API design, data integrity, and system thinking**.
