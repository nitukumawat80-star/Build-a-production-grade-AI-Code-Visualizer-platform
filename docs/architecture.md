# Architecture

## Style
- Clean Architecture
- Repository Pattern
- Domain-first services

## Backend Layers
1. API (FastAPI routes)
2. Application (use-cases and orchestration)
3. Domain (entities and service contracts)
4. Infrastructure (AST parsers, DB repositories, cache)

## Request Flow
1. Client submits code + language.
2. `AnalysisService` checks Redis cache.
3. AST parser converts code into normalized tree.
4. Analysis pipeline executes:
   - dry run timeline
   - variable and memory snapshots
   - call stack frames
   - complexity estimator
   - smell/bug detectors
   - DSA pattern classifier
   - optimization advisor
5. Result persisted in PostgreSQL and cached in Redis.
6. Frontend renders timeline with animation controls.

## Multi-Tenant SaaS
- Tenant-safe user history isolation.
- Usage metrics table for premium analytics.
- Stripe-compatible billing boundary (integration point in docs).

## Scaling
- API stateless pods behind load balancer.
- Dedicated worker queue for exports/narration jobs.
- Postgres primary + read replicas.
- Redis cluster for hot caching.
