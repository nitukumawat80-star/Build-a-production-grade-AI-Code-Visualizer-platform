# Deployment Guide

## Local
1. `cp .env.example .env`
2. `docker compose up --build`

## Production (Kubernetes)
1. Build and push images for frontend/backend.
2. Configure managed PostgreSQL and Redis.
3. Deploy backend with HPA (CPU + request latency).
4. Deploy frontend on CDN-backed edge platform.
5. Configure ingress, TLS, WAF, and rate limiting.
6. Run DB migrations in release pipeline.

## Observability
- OpenTelemetry traces for API handlers.
- Prometheus metrics:
  - request latency
  - parse latency by language
  - cache hit ratio
  - export queue depth
- Structured logs with trace IDs.

## Security
- Enforce JWT auth + RBAC middleware.
- Secrets from vault provider.
- Restrict code execution sandbox for dynamic dry run.
- Row-level tenant checks for multi-user isolation.
