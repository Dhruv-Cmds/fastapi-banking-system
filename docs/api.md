# Architecture

This document provides an overview of the project's endpoints.

---

## API Endpoints

## Admin — `/api/admin`

| Method | Endpoint                         | Auth | Description        |
| ------ | -------------------------------- | ---- | ------------------ |
| GET    | `/api/admin/users`               | ✅    | View all users     |
| GET    | `/api/admin/accounts`            | ✅    | View all accounts  |
| PUT    | `/api/admin/accounts/{account_id}/close` | ✅ | Close account |

## Authentication — `/api`

| Method | Endpoint      | Auth | Description           |
| ------ | ------------- | ---- | --------------------- |
| POST   | `/api/signup` | ❌    | Register user         |
| POST   | `/api/login`  | ❌    | Login and receive JWT |
| PUT    | `/api/me`     | ✅    | Update user profile   |

## Accounts — `/api/accounts`

| Method | Endpoint                     | Auth | Description      |
| ------ | ---------------------------- | ---- | ---------------- |
| POST   | `/api/accounts`              | ✅    | Create account   |
| GET    | `/api/accounts`              | ✅    | List accounts    |
| DELETE | `/api/accounts/{id}`         | ✅    | Delete account   |
| POST   | `/api/accounts/{id}/deposit` | ✅    | Deposit money    |
| POST   | `/api/accounts/{id}/withdraw` | ✅   | Withdraw money   |

## Transfers & Transactions — `/api`

| Method | Endpoint                         | Auth | Description              |
| ------ | -------------------------------- | ---- | ------------------------ |
| POST   | `/api/transfer`                  | ✅    | Transfer money           |
| GET    | `/api/transactions/{account_id}` | ✅    | View transaction history |

## Health — `/health`

| Method | Endpoint  | Auth | Description                   |
| ------ | --------- | ---- | ----------------------------- |
| GET    | `/health` | ❌    | Check API and database health |

The API includes a health monitoring endpoint for deployment and infrastructure checks.

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