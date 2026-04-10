# 🏦 FastAPI Banking System API

A clean and modular **Bank Account Management API** built using **FastAPI**, **SQLAlchemy**, and **MySQL**.
This project demonstrates core backend concepts including account creation, deposits, withdrawals, and fund transfers with proper validation and database handling.

---

## 🚀 Features

* Create bank accounts
* View all accounts
* Deposit money into an account
* Withdraw money with balance validation
* Transfer money between accounts
* Environment-based configuration (`.env`)
* SQLAlchemy ORM integration
* Clean project structure

---

## 🧱 Tech Stack

* **FastAPI** – Web framework
* **SQLAlchemy** – ORM for database interaction
* **MySQL** – Relational database
* **Pydantic** – Data validation
* **python-dotenv** – Environment variable management

---

## 📁 Project Structure

```

fastapi-banking-system/
│
├── routes/
│   └── account.py        # API routes
│
├── db.py                 # Database connection & session
├── models.py             # SQLAlchemy models (tables)
├── schemas.py            # Pydantic schemas
├── main.py               # App entry point
├── requirements.txt      # Dependencies
├── .env                  # Environment variables (not committed)
└── .gitignore

```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Dhruv-Cmds/fastapi-banking-system.git
cd fastapi-banking-system
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate it:

* Windows:

```bash
.venv\Scripts\activate
```

* Mac/Linux:

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=bankaccountsystem

```

---

### 5. Run the application

```bash
uvicorn main:app --reload
```

---

## 🧠 Database Behavior

* Tables are automatically created at startup using SQLAlchemy:

```python
models.Base.metadata.create_all(bind=engine)
```

* The table structure is derived directly from the models defined in `models.py`.

---

## 📌 API Endpoints

### ➕ Create Account

```
POST /accounts
```

### 📄 Get All Accounts

```
GET /accounts
```

### 💰 Deposit Money

```
POST /accounts/{id}/deposit
```

### 💸 Withdraw Money

```
POST /accounts/{id}/withdraw
```

### 🔄 Transfer Money

```
POST /transfer
```

---

## ⚠️ Validations Implemented

* Cannot transfer to the same account
* Amount must be greater than zero
* Cannot withdraw more than available balance
* Unique account number enforced

---

## 🔐 Security Note

* `.env` file is excluded from version control
* Passwords are URL-encoded using `quote_plus` to prevent connection issues

---


## ⭐ Conclusion

This project serves as a strong foundation for building scalable backend systems with clean architecture and proper database handling.

---
