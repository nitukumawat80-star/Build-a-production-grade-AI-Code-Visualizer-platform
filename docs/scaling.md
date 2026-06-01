# 100K+ User Scaling Strategy

## Capacity Model
- Peak concurrent users: 8k
- Peak API RPS: 1.5k
- P95 analysis latency target: < 1.8s (cache hit), < 4s (cold path)

## Scaling Techniques
- Shard analysis jobs by language profile.
- Cache identical code hashes in Redis for fast replay.
- Async queue for heavy operations (video/gif/pdf generation, narration).
- Read replicas for dashboard and historical analytics.
- Partition `usage_events` monthly for long-term analytics performance.

## SLOs
- Availability: 99.9%
- Analysis API error rate: < 0.5%
- Export completion success: > 99%

## Resilience
- Circuit breakers around external AI narration providers.
- Retry with idempotency keys for export jobs.
- Graceful degradation: return static timeline if advanced simulation is delayed.
