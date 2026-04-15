# 🏦 FastAPI Banking System API

A clean, modular, and production-style **Bank Account Management System** built using **FastAPI**, **SQLAlchemy**, and **MySQL**.

This project demonstrates real-world backend architecture including authentication, account management, transactions, and proper validation.

---

## 🖼️ UI Preview

![UI Preview](screenshots/ui_1.png)  
![UI Preview](screenshots/ui_2.png)

---

## 🚀 Features

### 🔐 Authentication
- User Signup & Login (JWT-based)
- Case-insensitive username handling
- Secure password hashing

### 🏦 Account Management
- Create multiple bank accounts
- Unique account number enforcement
- View all user accounts

### 💰 Transactions
- Deposit funds
- Withdraw funds with balance validation
- Transfer money between accounts
- Self-transfer prevention
- Concurrency-safe transactions (DB locking)

### 🧠 Validation & Logic
- Amount must be greater than zero
- Cannot withdraw more than balance
- Cannot transfer to same account
- Backend-driven validation

### ⚙️ System Design
- Environment-based configuration (`.env`)
- Clean modular structure
- SQLAlchemy ORM integration

---

## 🧱 Tech Stack

- **FastAPI** – High-performance backend framework  
- **SQLAlchemy** – ORM for database interaction  
- **MySQL** – Relational database  
- **Pydantic** – Data validation  
- **python-dotenv** – Environment configuration  
- **JWT (python-jose)** – Authentication  

---

## 📁 Project Structure

```
fastapi-banking-system/
│
├── app/
│ ├── routes/ # API routes (auth + accounts)
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── db/ # Database setup
│ ├── core/ # Security (JWT, hashing)
│ └── dependencies/ # Auth dependencies
│
├── main.py # App entry point
├── requirements.txt # Dependencies
├── .env # Environment variables (ignored)
└── .gitignore

```
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Dhruv-Cmds/fastapi-banking-system.git
cd fastapi-banking-system
```

### 2️⃣ Create virtual environment

```
python -m venv .venv
```

Windows
```
.venv\Scripts\activate
```

Mac/Linux
```
source .venv/bin/activate
```

3️⃣ Install dependencies
```
pip install -r requirements.txt
```

4️⃣ Configure environment variables

Create a .env file:

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=bankaccountsystem

SECRET_KEY=your_secret_key
ALGORITHM=HS256

5️⃣ Run the application

uvicorn main:app --reload

🧠 Database Behavior

Tables are automatically created at startup:
models.Base.metadata.create_all(bind=engine)
Schema is derived from SQLAlchemy models.

📌 API Endpoints

🔐 Auth

POST /signup
POST /login

🏦 Accounts

POST /accounts
GET  /accounts
💰 Transactions
POST /accounts/{id}/deposit
POST /accounts/{id}/withdraw
POST /transfer

⚠️ Validations Implemented

Cannot transfer to the same account
Amount must be greater than zero
Cannot withdraw more than balance
Unique account number enforced
Case-insensitive usernames
Secure transaction locking (prevents race conditions)

🔐 Security

JWT-based authentication
Password hashing (bcrypt)
.env excluded from Git
Secure DB connection handling

💎 Highlights

Clean architecture (modular FastAPI structure)
Real-world banking logic implementation
Proper separation of concerns
Scalable backend design

⭐ Conclusion

This project demonstrates how to build a real-world backend system with:

Authentication
Database design
Transaction safety
Clean architecture

It serves as a strong foundation for scaling into a full fintech application 🚀