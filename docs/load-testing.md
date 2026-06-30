# Load Testing

This document describes the load testing methodology, environment, benchmarking results, and scalability characteristics of the FastAPI Banking System.

---

# Overview

The API was load tested using **k6** against a production-style environment to evaluate performance under authenticated banking workloads.

The benchmark focuses on realistic API usage rather than isolated endpoint stress tests.

---

# Testing Environment

The load tests were executed using the following stack:

- FastAPI
- Async SQLAlchemy
- MySQL
- Redis
- Docker
- JWT Authentication
- bcrypt password hashing
- SlowAPI rate limiting
- Linux VPS

---

# VPS Specifications

| Component | Specification |
|-----------|---------------|
| CPU | 2 vCPU |
| Memory | 8 GB RAM |
| Operating System | Ubuntu 24.04 |
| Deployment | Docker |
| Database | MySQL 8 |
| Cache | Redis 7 |

---

# Load Testing Tool

The project uses **k6** for performance testing.

Features of the testing setup include:

- Concurrent virtual users
- Authenticated requests
- Banking workflow simulation
- Throughput measurement
- Latency observation
- Stability evaluation

---

# Running Load Tests

## Standard Load Test

```bash
k6 run load_test.js
```

---

## Full Banking Workflow

```bash
k6 run full_test.js
```

The full workflow simulates authenticated banking operations rather than repeatedly calling a single endpoint.

---

# Tested Workflows

The benchmark includes the following operations:

- User signup
- User login
- Account creation
- Deposits
- Withdrawals
- Transfers
- Transaction history
- Profile updates
- Account deletion
- Administrative endpoints

This provides a realistic representation of application usage under load.

---

# Performance Results

| Metric | Result |
|---------|---------|
| Requests per Second | ~534 req/s |
| Total HTTP Requests | 111k+ |
| Test Duration | 60 seconds |
| Virtual Users | 500 |
| Iterations Completed | 55k+ |
| Catastrophic Crashes | 0 |

These results were observed on the hardware configuration described above.

---

#  Load Testing Results

| Test                          | Virtual Users | Duration | Requests/sec | Result |
| ----------------------------- | ------------- | -------- | ------------ | ------ |
| Linux VPS Production Test     | 500 VUs       | 60s      | ~534 req/s   | Services remained operational |
| Banking Workflow Load Test    | 500 VUs       | 60s      | ~534 req/s   | 111k+ HTTP requests processed |
| Sustained Banking Sessions    | 500 VUs       | 60s      | Stable under moderate traffic | No catastrophic crashes |
| Transaction Workflow Test     | 500 VUs       | 60s      | Included Above | Deposits, withdrawals, transfers completed |

---


# Concurrent User Capacity

| Concurrent Users | System Behavior |
|------------------|-----------------|
| 1–200 | Stable with healthy response times |
| 200–300 | Stable under moderate authenticated traffic |
| 300–500 | Increased latency with rate limiting |
| 500+ | Overload behavior begins to appear |

The application continued operating throughout the benchmark without service failure.

---

# Scaling Behavior

During testing, the system demonstrated the following characteristics:

### Normal Load

- Low latency
- Stable response times
- Minimal queueing

---

### Moderate Load

- Increased CPU utilization
- Stable database connectivity
- Consistent request handling

---

### Heavy Load

- Higher response latency
- Rate limiting became more active
- Increased request queueing
- Services remained operational

---

### Extreme Load

Beyond approximately 500 virtual users:

- Additional latency
- More HTTP 429 responses
- Database contention
- No catastrophic crashes

---

# Bottleneck Analysis

Several factors contributed to reduced performance under heavy load.

| Bottleneck | Cause |
|------------|-------|
| Password hashing | bcrypt is CPU intensive |
| Database connections | Limited connection pool |
| Single MySQL instance | Write-heavy workload |
| Request queueing | High concurrent traffic |
| Rate limiting | SlowAPI protecting services |

These bottlenecks are expected in a single-node deployment.

---

# Related Documentation

- `README.md`
- `testing.md`
- `performance.md`
- `deployment.md`