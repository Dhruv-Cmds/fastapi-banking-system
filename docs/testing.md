# Testing

This document describes the project's testing strategy, test environment, and load testing workflow.

---

# Overview

The FastAPI Banking System includes a comprehensive asynchronous test suite designed to validate authentication, authorization, account operations, and transaction workflows.

The project uses **pytest** together with **pytest-asyncio** to test asynchronous endpoints and database interactions.

---

# Testing Stack

| Component | Technology |
|-----------|------------|
| Test Runner | Pytest |
| Async Testing | pytest-asyncio |
| HTTP Client | HTTPX |
| Database | MySQL |
| ORM | SQLAlchemy 2.x Async |
| Authentication | JWT |
| Environment | Docker / Local |

---

# Test Environment

The application supports dedicated testing environments using separate database and Redis instances.

Example configuration:

```env
ENV=test

DB_HOST=127.0.0.1
DB_PORT=3306

DB_NAME=banking_test
DB_USER=banking_user
DB_PASSWORD=your_password

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=1
REDIS_PASSWORD=changeme

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Using a dedicated database prevents tests from affecting development or production data.

---

# Running Tests

## Local Development

Run the full test suite:

```bash
export ENV=test

python -m pytest -v
```

---

## Inside Docker (Shared Infrastructure)

```bash
docker exec -it banking-api bash

export ENV=docker

python -m pytest -v
```

Tests connect to:

```
shared-mysql:3306
shared-redis:6379
```

---

## Inside Docker (Standalone)

```bash
docker compose -f docker-compose.oss.yml exec banking-api bash

export ENV=docker

python -m pytest -v
```

Tests connect to:

```
mysql:3306
redis:6379
```

---

# Test Coverage

The current test suite validates:

## Authentication

- User signup
- User login
- JWT generation
- Invalid credentials
- Protected endpoints

---

## Authorization

- User permissions
- Admin permissions
- RBAC validation
- Unauthorized access

---

## Account Management

- Account creation
- Retrieve user accounts
- Account ownership validation
- Account lifecycle

---

## Transactions

- Deposits
- Withdrawals
- Transfers
- Balance updates
- Transaction history

---

## Administration

Administrative endpoint testing includes:

- View users
- View accounts
- Close accounts
- Role protection

---

# Database Testing

The test suite uses a dedicated MySQL database.

Testing includes:

- Database transactions
- Constraint validation
- Rollback behavior
- Async session handling
- Connection management

Each test runs independently to reduce interference between test cases.

---

# Async Testing

The application is fully asynchronous.

Testing covers:

- Async API endpoints
- Async database sessions
- Async fixtures
- Dependency overrides
- Event loop compatibility

---

# Async Fixes

Several improvements were implemented to improve reliability across environments.

## Issues Addressed

- Windows event loop compatibility
- Cross-event-loop database errors
- Connection leaks
- Async engine isolation
- Per-test database sessions

These changes improve consistency between local development, Docker, and Linux deployments.

---

# Dependency Overrides

Tests replace production dependencies where appropriate.

Examples include:

- Database sessions
- Authentication dependencies
- Application settings

This allows tests to remain isolated from production resources.

---

# Test Workflow

```
Start Test Environment
          │
          ▼
Create Test Database
          │
          ▼
Run Test Suite
          │
          ▼
Validate Results
          │
          ▼
Cleanup Resources
```

---

# Continuous Integration

The project integrates testing into the GitHub Actions CI/CD pipeline.

Each workflow can automatically:

- Install dependencies
- Execute the test suite
- Validate application integrity
- Prevent broken code from being deployed

---

# Best Practices

- Use a dedicated test database.
- Never run tests against production data.
- Keep tests independent and repeatable.
- Isolate database sessions between tests.
- Validate both successful and failure scenarios.
- Test authentication before protected endpoints.
- Include regression tests for bug fixes.

---

# Future Improvements

Potential enhancements include:

- Increased test coverage
- Integration testing
- End-to-end frontend testing
- Performance regression testing
- Mutation testing
- Automated coverage reports

---

# Related Documentation

- `README.md`
- `docker.md`
- `deployment.md`
- `load-testing.md`
- `performance.md`