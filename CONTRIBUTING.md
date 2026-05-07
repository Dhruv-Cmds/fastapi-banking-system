# Contributing to FastAPI Banking System

Thanks for your interest in contributing! This guide will help you get started.

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.11+
- MySQL 8.0+
- Node.js 18+
- Docker (optional but recommended)

### 1. Clone the repo
```bash
git clone https://github.com/Dhruv-Cmds/fastapi-banking-system.git
cd fastapi-banking-system
```

### 2. Backend setup
```bash
pip install -r requirements.txt
cp docker/.env.example docker/.env
# Fill in your DB credentials in docker/.env
```

### 3. Frontend setup
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env if needed
```

### 4. Run with Docker (easiest)
```bash
docker-compose up --build
```

### 5. Run backend locally
```bash
cd backend
$env:ENV="dev"        # Windows
export ENV=dev        # Linux/Mac
uvicorn main:app --reload
```

---

## 🧪 Running Tests
```bash
$env:ENV="test"       # Windows
export ENV=test       # Linux/Mac
cd backend
pytest -v
```

Make sure your test DB is running and `TEST_DB_NAME` is set in your `.env`.

---

## 📬 Submitting a PR

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests and make sure they pass
5. Push and open a Pull Request against `main`
6. Describe what you changed and why

---

## 🐛 Reporting Issues

Open a GitHub Issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your OS and Python version

---

## 📌 Good First Issues

Look for issues tagged [`good first issue`](https://github.com/Dhruv-Cmds/fastapi-banking-system/issues?q=is%3Aissue+label%3A%22good+first+issue%22) — these are beginner friendly and a great place to start.