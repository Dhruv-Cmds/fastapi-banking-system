# 🤝 Contributing to FastAPI Banking System

Thanks for your interest in contributing to this project 💙

This repository welcomes contributions from:
- beginners learning open source
- backend developers
- frontend contributors
- DevOps learners
- documentation writers
- performance enthusiasts

You can contribute by:
- fixing bugs
- improving documentation
- adding tests
- building features
- improving frontend UX
- optimizing backend performance

If you're new to open source, start with issues labeled:
- `good first issue`
- `help wanted`

---

# 🏗️ Project Structure

```text
backend/
├── routes/
├── services/
├── models/
├── schemas/
├── dependencies/
├── core/
└── tests/

frontend/
docker/
```

---

# 🛠️ Local Setup

## Prerequisites

- Python 3.11+
- MySQL 8.0+
- Node.js 18+
- Docker (optional but recommended)

---

## 1. Clone the Repository

```bash
git clone https://github.com/Dhruv-Cmds/fastapi-banking-system.git
cd fastapi-banking-system
```

---

## 2. Backend Setup

```bash
pip install -r requirements.txt
```

Create:

```text
docker/.env
```

Then add your environment variables.

Example:

```env
ENV=dev

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3008
DB_NAME=banking

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 3. Frontend Setup

```bash
cd frontend
npm install
```

Create:

```text
frontend/.env
```

Add your frontend environment variables if required.

---

## 4. Run with Docker (Recommended)

```bash
docker-compose up --build
```

---

## 5. Run Backend Locally

### Windows

```powershell
cd backend
$env:ENV="dev"
uvicorn main:app --reload
```

### Linux / macOS

```bash
cd backend
export ENV=dev
uvicorn main:app --reload
```

---

# 🧪 Running Tests

### Windows

```powershell
$env:ENV="test"
cd backend
pytest -v
```

### Linux / macOS

```bash
export ENV=test
cd backend
pytest -v
```

Make sure your test database is running and configured correctly.

---

# 📬 Pull Request Guidelines

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/your-feature-name
```

Example:

```bash
git checkout -b fix/transaction-pagination
```

3. Make your changes
4. Run tests
5. Commit your changes
6. Push your branch
7. Open a Pull Request against `main`

---

# ✅ PR Expectations

Please keep pull requests:
- focused on a single feature or fix
- clearly described
- reasonably small when possible

Large unrelated refactors may be difficult to review.

---

# 🐛 Reporting Issues

When opening an issue, include:

- expected behavior
- actual behavior
- steps to reproduce
- operating system
- Python version
- logs/screenshots if applicable

---

# 🔐 Security Issues

Please avoid publicly disclosing serious security vulnerabilities.

Instead, open a private discussion or contact the maintainer directly.

---

# 📌 Good First Issues

Look for issues labeled:

- `good first issue`
- `help wanted`

These are beginner-friendly tasks and a great place to start contributing.

Example:

https://github.com/Dhruv-Cmds/fastapi-banking-system/issues?q=is%3Aissue+label%3A%22good+first+issue%22

---

# 🧠 Development Guidelines

## Backend
- Follow FastAPI best practices
- Use async-safe patterns
- Keep services modular
- Add type hints where possible

## Frontend
- Keep components reusable
- Maintain responsive UI
- Avoid unnecessary dependencies

---

# 🚫 Please Avoid

- massive unrelated PRs
- hardcoded secrets
- unnecessary dependency additions
- breaking API changes without discussion

---

# 🌱 Open Source Philosophy

This project is intentionally contributor-friendly.

The goal is to:
- encourage learning
- provide real-world backend experience
- allow experimentation
- help developers contribute to open source comfortably

Contributors are encouraged to:
- improve architecture
- optimize performance
- add features
- improve developer experience

---

# 🙌 Thanks

Every contribution matters.

Even small fixes help improve the project for future contributors and learners.

Happy coding 🚀