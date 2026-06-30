# Architecture

This document provides an overview of the project's architecture, design principles, and core application modules.

---

# System Overview

The application follows a layered architecture to keep business logic, API routes, and data access cleanly separated. This improves maintainability, scalability, and testability while making it easier to extend the project with new features.

```
                   Client
                      │
                HTTP / JSON
                      │
              FastAPI Application
                      │
      ┌───────────────┼────────────────┐
      │               │                │
 Authentication   Business Logic   Middleware
      │               │                │
      └───────────────┼────────────────┘
                      │
               Service Layer
                      │
              Repository Layer
               │             │
               │             │
      SQLAlchemy ORM     Redis Cache
               │             ▲
               └──────┬──────┘
                      │
                    MySQL
```

---

# Request Lifecycle

A typical request flows through the application in the following order:

```
Client
   │
   ▼
FastAPI Route
   │
   ▼
Authentication & Authorization
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
SQLAlchemy Async ORM
   │
   ▼
MySQL / Redis
   │
   ▼
Response
```

Each layer has a single responsibility, reducing coupling between application components.

---

# Design Principles

The project is built around several architectural principles:

- Async-first backend design
- Layered service architecture
- Separation of concerns
- Repository pattern for data access
- Configuration-driven business rules
- Stateless JWT authentication
- Redis-backed caching
- Production-ready Docker deployment

---

# Project Layers

## API Layer

The API layer exposes REST endpoints using FastAPI.

Responsibilities include:

- Request validation
- Response serialization
- Dependency injection
- Authentication
- Authorization
- HTTP status handling

Business logic is intentionally kept out of the route handlers.

---

## Service Layer

The Service Layer contains the application's business logic.

Responsibilities include:

- Account operations
- Transaction processing
- Validation
- Business rules
- Coordinating repository operations

This layer keeps route handlers lightweight and reusable.

---

## Repository Layer

The Repository Layer handles communication with the database.

Responsibilities include:

- CRUD operations
- Query abstraction
- Data persistence
- Database interaction

Separating repositories from services makes testing significantly easier.

---

## Database Layer

Persistent data is stored in MySQL using SQLAlchemy 2.x Async ORM.

Current entities include:

- User
- Account
- Transaction

Relationships are implemented using SQLAlchemy ORM with foreign key constraints and ownership validation.

---

## Cache Layer

Redis is used to improve performance by reducing unnecessary database queries.

Current responsibilities include:

- Frequently accessed data caching
- Shared infrastructure support
- Future session and rate-limiting extensions

---

# Domain Model

The banking system currently consists of three primary entities.

```
User
 │
 ├── Account
 │      │
 │      ├── Deposit
 │      ├── Withdraw
 │      └── Transfer
 │
 └── Transaction History
```

## User

Represents an authenticated application user.

A user can own multiple bank accounts.

---

## Account

Represents an individual bank account.

Each account contains:

- Unique account number
- Balance
- Status
- Owner

Current account states:

```
ACTIVE
CLOSED
```

Closed accounts are blocked from financial operations.

---

## Transaction

Every financial operation creates a transaction record.

Supported transaction types include:

- Deposit
- Withdrawal
- Transfer

Each transaction is stored permanently to provide an audit trail.

---

# Core Modules

## Authentication

Authentication is implemented using JWT tokens.

Features include:

- User signup
- User login
- Password hashing using bcrypt
- Protected routes
- JWT access tokens

---

## Authorization

Role-Based Access Control (RBAC) protects privileged endpoints.

Supported roles include:

- User
- Admin

Administrative operations are restricted to authorized users.

---

## Account Management

Features include:

- Create accounts
- View accounts
- Multiple accounts per user
- Account ownership validation
- Soft account closure

---

## Transactions

Supported operations include:

- Deposit
- Withdraw
- Transfer

All transaction operations are executed using atomic database transactions to ensure consistency.

---

## Administration

Administrative functionality includes:

- View all users
- View all accounts
- Close accounts
- Protected admin endpoints

---

# Business Rules

The application enforces several validation rules to maintain data integrity.

Examples include:

- Prevent negative balances
- Prevent self-transfers
- Only ACTIVE accounts can perform transactions
- Configurable deposit limits
- Configurable withdrawal limits
- Configurable transfer limits

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| API | FastAPI |
| ORM | SQLAlchemy 2.x Async |
| Database | MySQL |
| Cache | Redis |
| Authentication | JWT |
| Authorization | RBAC |
| Password Hashing | bcrypt + passlib |
| Validation | Pydantic |
| Containerization | Docker |
| Reverse Proxy | Nginx |

---

# Architecture Highlights

- Fully asynchronous request handling
- Layered service architecture
- Repository pattern
- JWT-secured API
- RBAC authorization
- Async SQLAlchemy integration
- Redis caching support
- Dockerized infrastructure
- Production-ready deployment design
- Configuration-driven business rules

---

# Future Improvements

The architecture is designed to support future enhancements, including:

- Background task queues
- WebSocket notifications
- Horizontal scaling
- Database replication
- Distributed caching
- Event-driven architecture
- Observability with Grafana and Prometheus

---

# Related Documentation

- `README.md`
- `docs/docker.md`
- `docs/deployment.md`
- `docs/security.md`
- `docs/testing.md`
- `docs/load-testing.md`
- `docs/performance.md`