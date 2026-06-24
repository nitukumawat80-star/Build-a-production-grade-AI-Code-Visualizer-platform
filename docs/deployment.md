# Deployment Guide

## Local
1. `cp .env.example .env`
2. `docker compose up --build`
3. Open `http://localhost:3000`.

The frontend calls `/api/backend/*` by default. Next.js proxies those requests to
`BACKEND_API_BASE_URL`, which should point at the backend from the frontend
runtime. In Docker this is `http://backend:8000/api/v1`.

Useful local environment values:

```env
BACKEND_API_BASE_URL=http://backend:8000/api/v1
NEXT_PUBLIC_API_BASE_URL=/api/backend
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Production (Kubernetes)
1. Build and push images for frontend/backend.
2. Configure managed PostgreSQL and Redis.
3. Deploy backend with HPA (CPU + request latency).
4. Deploy frontend on CDN-backed edge platform.
5. Configure ingress, TLS, WAF, and rate limiting.
6. Run DB migrations in release pipeline.

For Cloud Run-style deployments, set the frontend service variables like this:

```env
BACKEND_API_BASE_URL=https://YOUR_BACKEND_SERVICE_URL/api/v1
NEXT_PUBLIC_API_BASE_URL=/api/backend
```

This keeps browser requests same-origin while the Next.js server proxies them to
the backend service.

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
