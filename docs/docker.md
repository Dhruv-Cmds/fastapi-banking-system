# Docker

This document explains the available Docker workflows for running the FastAPI Banking System in development and production environments.

---

# Overview

The project supports two Docker deployment modes:

1. **Shared Infrastructure (Recommended)**
2. **Standalone Docker**

The recommended approach uses a separate infrastructure repository that provides shared MySQL and Redis containers for multiple projects. The standalone option runs everything directly from this repository.

---

# Docker Architecture

## Shared Infrastructure

```
                    +----------------------+
                    |   FastAPI Backend    |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |   Shared MySQL       |
                    +----------------------+
                               |
                    +----------v-----------+
                    |   Shared Redis       |
                    +----------------------+
                               |
                    +----------v-----------+
                    | React + Vite Frontend|
                    +----------------------+
```

This setup allows multiple projects to share the same infrastructure while keeping each application isolated.

---

## Standalone Deployment

```
+------------------------------+
| FastAPI Banking System       |
|------------------------------|
| Backend                      |
| Frontend                     |
| MySQL                        |
| Redis                        |
+------------------------------+
```

Everything runs from a single repository using Docker Compose.

---

# Shared Infrastructure (Recommended)

This workflow uses the separate **docker-infra** repository to provide common infrastructure for multiple applications.

## Advantages

- Shared MySQL instance
- Shared Redis instance
- Reduced resource usage
- Easier management across projects
- Cleaner separation between infrastructure and application code

## Start Infrastructure

```bash
cd docker-infra

docker compose up -d
```

Once the infrastructure is running, start the application:

```bash
cd fastapi-banking-system

docker compose up --build
```

The application automatically connects to the shared containers.

---

# Standalone Docker

If you don't want to use the shared infrastructure repository, the project can run independently.

Start everything using:


```bash
docker compose -f docker-compose.oss.yml up --build
```

This starts:

- FastAPI backend
- React frontend
- MySQL
- Redis

No external repositories are required.

---

# Docker Compose Files

## docker-compose.yml

Uses the shared infrastructure.

Services include:

- Backend
- Frontend

External services:

- Shared MySQL
- Shared Redis

---

## docker-compose.oss.yml

Runs a completely self-contained environment.

Services include:

- Backend
- Frontend
- MySQL
- Redis

Suitable for:

- Open-source users
- Local development
- Portfolio demonstrations

---

# Environment Configuration

The application selects the correct infrastructure based on environment variables.

## Shared Infrastructure

```
ENV=docker

DB_HOST=shared-mysql
REDIS_HOST=shared-redis
```

---

## Standalone

```
ENV=docker

DB_HOST=mysql
REDIS_HOST=redis
```

---

## Local Development

```
ENV=dev

DB_HOST=127.0.0.1
REDIS_HOST=127.0.0.1
```

---

# Starting the Project

## Shared Infrastructure

Start infrastructure:

```bash
cd docker-infra

docker compose up -d
```

Start the application:

```bash
cd fastapi-banking-system

docker compose up --build
```

---

## Standalone

```bash
docker compose -f docker-compose.oss.yml up --build
```

---

# Stopping Containers

## Shared Infrastructure

Application only:

```bash
docker compose down
```

Infrastructure:

```bash
cd docker-infra

docker compose down
```

---

## Standalone

```bash
docker compose -f docker-compose.oss.yml down
```

---

# Reset Database

## Shared Infrastructure

```bash
cd docker-infra

docker compose down -v
```

This removes:

- Shared MySQL data
- Shared Redis data

> **Warning:** This affects every project using the shared infrastructure.

---

## Standalone

```bash
docker compose -f docker-compose.oss.yml down -v
```

This removes only this project's database and Redis volumes.

---

# Running Tests Inside Docker

## Shared Infrastructure

```bash
docker exec -it banking-api bash

export ENV=docker

python -m pytest -v
```

The tests connect to:

```
shared-mysql:3306
shared-redis:6379
```

---

## Standalone

```bash
docker compose -f docker-compose.oss.yml exec banking-api bash

export ENV=docker

python -m pytest -v
```

The tests connect to:

```
mysql:3306
redis:6379
```

---

# Docker Images

The project includes Dockerfiles for:

- FastAPI backend
- React frontend

These images are used for:

- Local development
- Production deployments
- GitHub Actions CI/CD
- VPS deployments

---

# Development Workflow

```
Clone Repository
        │
        ▼
Configure .env
        │
        ▼
Choose Docker Mode
        │
        ├──────────────┐
        ▼              ▼
 Shared Infra     Standalone
        │              │
        ▼              ▼
docker compose up --build
        │
        ▼
Application Ready
```

---

# Best Practices

- Use the shared infrastructure for active development.
- Use the standalone configuration for open-source users.
- Keep secrets in environment variables.
- Avoid modifying Dockerfiles unless necessary.
- Rebuild containers after dependency changes.
- Use Docker volumes to persist MySQL data.

---

# Related Documentation

- `README.md`
- `deployment.md`
- `testing.md`
- `security.md`