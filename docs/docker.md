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

Recommended for open source users or isolated development environments.

Services started:

* FastAPI
* MySQL
* Redis

Everything runs inside Docker Compose.

```text
           Docker Compose
                  │
     ┌────────────┼────────────┐
     │            │            │
 FastAPI       MySQL        Redis
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

Services are provided externally:

* MySQL
* Redis

Only the application container is started by this repository.

```text
Application Container
        │
        ├──────────────► Shared MySQL
        │
        └──────────────► Shared Redis
```

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

# Project Structure


| File                   | Purpose                        |
| ---------------------- | ------------------------------ |
| docker-compose.yml     | Uses shared infrastructure     |
| docker-compose.oss.yml | Complete standalone deployment |
| docker/                | Dockerfiles                    |
| backend/               | Backend source code            |

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

# Networking

Docker Compose creates an isolated bridge network for service communication.

```text
                 Docker Network
                       │
       ┌───────────────┼───────────────┐
       │               │               │
   FastAPI          MySQL          Redis
```

Container communication uses service names instead of IP addresses.

Example:

```env
DB_HOST=mysql

REDIS_HOST=redis
```

---

# Volumes

Persistent Docker volumes are used to retain database data.

Example:

```text
mysql_data
```

Benefits:

* Data survives container recreation
* Easy backups
* Improved reliability

---

# Common Docker Commands

| Command                  | Description                |
| ------------------------ | -------------------------- |
| `docker compose up`      | Start services             |
| `docker compose up -d`   | Start in background        |
| `docker compose down`    | Stop and remove containers |
| `docker compose restart` | Restart services           |
| `docker compose logs`    | View logs                  |
| `docker compose logs -f` | Follow logs                |
| `docker compose ps`      | Show service status        |
| `docker compose build`   | Build images               |
| `docker image ls`        | List images                |
| `docker volume ls`       | List volumes               |
| `docker network ls`      | List networks              |

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