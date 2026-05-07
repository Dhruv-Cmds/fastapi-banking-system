````md id="contrib7"
# Contributing to FastAPI Banking System

Thanks for your interest in contributing! This guide will help you get started.

---

# 🛠️ Local Setup

## Prerequisites

- Python 3.11+
- MySQL 8.0+
- Node.js 18+
- Docker (optional but recommended)

---

## 1. Clone the Repository

```bash id="clone1"
git clone https://github.com/Dhruv-Cmds/fastapi-banking-system.git
cd fastapi-banking-system
````

---

## 2. Backend Setup

```bash id="backend1"
pip install -r requirements.txt
cp docker/.env.example docker/.env
```

Fill in your database credentials inside `docker/.env`.

---

## 3. Frontend Setup

```bash id="frontend1"
cd frontend
npm install
cp .env.example .env
```

Edit `.env` if needed.

---

## 4. Run with Docker (Recommended)

```bash id="docker1"
docker-compose up --build
```

---

## 5. Run Backend Locally

### Windows

```powershell id="win1"
cd backend
$env:ENV="dev"
uvicorn main:app --reload
```

### Linux / macOS

```bash id="linux1"
cd backend
export ENV=dev
uvicorn main:app --reload
```

---

# 🧪 Running Tests

### Windows

```powershell id="testwin1"
$env:ENV="test"
cd backend
pytest -v
```

### Linux / macOS

```bash id="testlinux1"
export ENV=test
cd backend
pytest -v
```

Make sure your test database is running and `TEST_DB_NAME` is configured in your `.env`.

---

# 📬 Submitting a Pull Request

1. Fork the repository
2. Create a new branch

```bash id="branch1"
git checkout -b feature/your-feature-name
```

3. Make your changes
4. Run tests and ensure they pass
5. Push your branch
6. Open a Pull Request against `main`
7. Clearly describe what changed and why

---

# 🐛 Reporting Issues

When opening an issue, include:

* What you expected to happen
* What actually happened
* Steps to reproduce
* Your operating system
* Python version

---

# 📌 Good First Issues

Look for issues tagged `good first issue`.

These are beginner-friendly tasks and a great place to start contributing:

https://github.com/Dhruv-Cmds/fastapi-banking-system/issues?q=is%3Aissue+label%3A%22good+first+issue%22

```
```
