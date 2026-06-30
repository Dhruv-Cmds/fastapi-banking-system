# Deployment

This document describes the production deployment architecture, infrastructure, and deployment workflow used for the FastAPI Banking System.

---

# Overview

The application is deployed on a Linux VPS (Ubantu) using Docker containers behind an Nginx reverse proxy with HTTPS enabled through Let's Encrypt.

The deployment is designed to resemble a real-world production environment while remaining simple to manage and extend.

---

# Production Architecture

```
                    Internet
                        │
                        ▼
                 Nginx Reverse Proxy
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 React Frontend                  FastAPI Backend
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
                    MySQL Database                 Redis Cache
```

---

# Infrastructure

The production environment currently consists of:

- Hostinger VPS
- Ubuntu 24.04 LTS
- Docker Engine
- Docker Compose
- Nginx Reverse Proxy
- FastAPI Backend
- React + Vite Frontend
- MySQL 8
- Redis 7
- GitHub Actions
- Let's Encrypt SSL Certificates

---

# Production Stack

## Backend

- FastAPI
- Async SQLAlchemy
- JWT Authentication
- Role-Based Access Control (RBAC)
- Uvicorn
- Docker

---

## Frontend

- React
- Vite
- Docker
- Nginx integration

---

## Database

- MySQL 8
- Persistent Docker volumes

---

## Cache

- Redis 7
- Shared infrastructure support

---

## Reverse Proxy

Nginx is responsible for:

- HTTPS termination
- Reverse proxy
- Static frontend delivery
- Routing requests to the backend
- Production isolation

---

# Deployment Workflow

Application updates are automatically deployed through GitHub Actions.

```
Developer
     │
     ▼
git push origin main
     │
     ▼
GitHub Actions
     │
     ▼
SSH into VPS
     │
     ▼
git pull
     │
     ▼
docker compose up --build -d
     │
     ▼
Production Updated
```

This workflow ensures deployments are repeatable and minimizes manual intervention.

---

# Deployment Steps

## 1. Push Changes

```bash
git add .

git commit -m "Update application"

git push origin main
```

---

## 2. GitHub Actions

The CI/CD pipeline automatically:

- Checks out the repository
- Connects to the VPS over SSH
- Pulls the latest changes
- Rebuilds containers
- Restarts the application

---

## 3. Docker Rebuild

The production server rebuilds containers using:

```bash
docker compose up --build -d
```

Updated containers replace the previous versions with minimal downtime.

---

# HTTPS

HTTPS certificates are managed using:

- Certbot
- Let's Encrypt

Benefits include:

- Encrypted communication
- Browser trust
- Secure JWT transmission

---

# Production Environment

Typical production components include:

```
Frontend
Backend
MySQL
Redis
Nginx
SSL Certificates
Docker Networks
Persistent Volumes
```

Each service is isolated within Docker while communicating over internal Docker networks.

---

# Public Access

Only the frontend is intended to be publicly accessible.

Public users can access:

- React application
- Public authentication endpoints

Internal services remain private.

---

# Restricted Components

The following are not publicly exposed:

- MySQL
- Redis
- Internal Docker network
- Production environment variables
- Server administration
- SSH access

Swagger and ReDoc are also disabled in production.

---

# Environment Management

Separate environment configurations are used for:

- Local development
- Docker development
- Testing
- Production

This allows the application to select the appropriate database, Redis host, and runtime settings.

---

# Production Configuration

Production deployment includes:

- Docker containers
- Shared infrastructure
- Persistent database storage
- HTTPS
- Reverse proxy
- JWT authentication
- RBAC authorization
- Rate limiting
- Environment-based configuration

---

# CI/CD Pipeline

GitHub Actions automates deployment by:

1. Triggering on pushes to the main branch.
2. Connecting securely to the VPS.
3. Updating the repository.
4. Rebuilding Docker containers.
5. Restarting services.

This reduces manual deployment steps and helps maintain consistency between releases.

---

# Deployment Checklist

Before deploying:

- Application builds successfully.
- Tests pass.
- Environment variables are configured.
- Docker Compose configuration is valid.
- SSL certificates are active.
- Database migrations (if applicable) are complete.

---

# Monitoring

Current deployment includes basic operational monitoring through:

- Docker container status
- Application logs
- Nginx logs
- GitHub Actions workflow status

Future improvements may include:

- Prometheus
- Grafana
- Centralized log aggregation
- Health monitoring dashboards

---

# Future Improvements

Potential deployment enhancements include:

- Blue-Green deployments
- Rolling updates
- Zero-downtime deployments
- Kubernetes support
- Docker Swarm support
- Database replication
- Automatic backups
- Horizontal scaling
- Multi-region deployments

---

# Related Documentation

- `README.md`
- `docker.md`
- `security.md`
- `testing.md`
- `load-testing.md`
- `performance.md`