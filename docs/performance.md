# Overview

The FastAPI Banking System is designed as an asynchronous application using FastAPI, SQLAlchemy Async, MySQL, and Redis. Performance improvements focus on maximizing throughput while maintaining data consistency and application stability.

---

# Bottleneck Analysis

Load testing identified several areas that influence application performance under heavy traffic.

| Bottleneck              | Description                                                             |
|------------------------ |-------------------------------------------------------------------------|
| bcrypt Password Hashing | CPU-intensive during authentication requests.                           |
| MySQL Connection Pool   | Concurrent write operations can exhaust available database connections. |
| Single MySQL Instance   | All write traffic is handled by a single database node.                 | 
| Request Queueing        | Worker saturation increases response latency under heavy load.          |
| Rate Limiting           | SlowAPI intentionally throttles excessive authenticated traffic.        |

# Benchmark Notes

- These bottlenecks are expected for a single-node deployment and represent opportunities for future scaling.

- These benchmarks were performed under a specific environment and should not be interpreted as universal performance guarantees.

Performance depends on several factors, including:

- Hardware resources
- Database configuration
- Network latency
- Docker resource limits
- Authentication workload
- Traffic patterns

Real-world deployments may produce different results.

---

---

# Optimizations Applied

Several improvements have already been implemented to increase stability and throughput.

## Backend

- Fully asynchronous FastAPI application
- Async SQLAlchemy ORM
- Connection pooling
- Repository pattern
- Service layer architecture

---

## Infrastructure

- Dockerized deployment
- Shared MySQL infrastructure
- Shared Redis infrastructure
- Persistent Docker volumes
- Internal Docker networking

---

## Performance

- Redis caching
- Async database operations
- MySQL-only architecture
- HTTPS termination through Nginx
- Rate limiting
- Optimized Docker networking

---

## Security

- JWT Authentication
- RBAC authorization
- bcrypt password hashing
- Production environment isolation

---

# Stability Summary

| Metric                       | Observation              |
|------------------------------|--------------------------|
| Maximum Tested Virtual Users | 500                      |
| Services Available           | Yes                      |
| Container Crashes            | None                     |
| Database Stability           | Stable                   |
| API Availability             | Maintained               |
| Service Recovery             | Automatic through Docker |

The application remained operational throughout stress testing without catastrophic failure.

---

# Capacity Summary

Estimated capacity based on the current infrastructure:

| Environment              | Estimated Concurrent Users |
|--------------------------|---------------------------:|
| Docker Desktop (Windows) | 200–300                    |
| Linux VPS                | 300–500                    |

Actual capacity depends on workload, authentication frequency, hardware resources, and database performance.

---

# Key Learnings

Developing this project provided practical experience with:

- Designing asynchronous APIs using FastAPI
- Managing async database sessions
- Preventing connection pool exhaustion
- Implementing transactional consistency
- Building layered service architectures
- Optimizing Docker networking
- Deploying applications to Linux VPS environments
- Benchmarking APIs with k6
- Identifying infrastructure bottlenecks
- Implementing production hardening with HTTPS, Nginx, and firewalls

---

# Current Limitations

The current deployment intentionally prioritizes simplicity over distributed scalability.

Known limitations include:

- Single FastAPI instance
- Single MySQL instance
- Single Redis instance
- No Redis Sentinel or Cluster
- No database replication
- No horizontal scaling
- No distributed task queue
- Limited by database connection pool size

These limitations are acceptable for portfolio projects, small deployments, and educational environments.

---

# Future Improvements

Potential enhancements include:

## Scalability

- Horizontal API scaling
- Load balancing
- Kubernetes deployment
- Docker Swarm support

---

## Database

- Read replicas
- Database replication
- Automatic backups
- Connection pool tuning

---

## Infrastructure

- Distributed Redis
- Background task queues
- Message brokers
- Object storage integration

---

## Observability

- Prometheus
- Grafana
- Centralized logging
- Distributed tracing
- Application metrics dashboards

---

# Conclusion

The project demonstrates a production-style asynchronous backend capable of handling moderate authenticated workloads within a single-node deployment.

The architecture provides a strong foundation for future scaling while remaining simple to understand, deploy, and extend.

---

# Related Documentation

- `README.md`
- `deployment.md`
- `load-testing.md`
- `testing.md`