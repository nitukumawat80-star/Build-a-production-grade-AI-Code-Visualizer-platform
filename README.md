# AI Code Visualizer SaaS

Production-grade, startup-ready AI code visualization platform for Python, Java, C++, and JavaScript.

## Highlights
- AST-driven code analysis across 4 languages.
- Dry run timeline with variable tracking, call stack, memory state, and output prediction.
- Complexity estimation (time + space), code smell/bug detection, optimization suggestions.
- DSA pattern detector: arrays, strings, linked lists, trees, graphs, DP, greedy, sliding window, two pointers.
- Animated visualization timeline controls: play, pause, next, previous, scrubber.
- AI narration preparation in English and Hindi.
- Optional Google Gemini enhancement layer for richer narration and insights.
- Export pipeline contracts for MP4, GIF, and PDF.
- Premium dashboard with analytics and user history.
- Clean architecture, repository pattern, Docker, CI/CD-ready, PostgreSQL + Redis.

## Tech Stack
- Frontend: Next.js 14, TypeScript, TailwindCSS, Framer Motion, Monaco Editor.
- Backend: FastAPI, Python 3.12.
- Data: PostgreSQL, Redis.

## Quick Start
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Run stack:
   ```bash
   docker compose up --build
   ```
3. Open:
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs

## Fetch Troubleshooting
- Frontend uses `NEXT_PUBLIC_API_BASE_URL=/api/backend` by default.
- Next.js proxies `/api/backend/*` to `BACKEND_API_BASE_URL`.
- For Docker, keep `BACKEND_API_BASE_URL=http://backend:8000/api/v1`.
- For Cloud Run, set `BACKEND_API_BASE_URL=https://YOUR_BACKEND_URL/api/v1`.
- If analysis says backend connection failed, check that the backend service is running and this URL is reachable from the frontend runtime.

## Gemini Setup (Optional)
1. Create Gemini API key from [Google AI Studio](https://ai.google.dev/).
2. Add in `.env`:
   - `GEMINI_API_KEY=your_key`
   - `GEMINI_MODEL=gemini-2.5-flash`
3. In UI, choose `AI Provider = Google Gemini`.

## Monorepo Layout
- `backend/`: FastAPI services, domain logic, AST analysis.
- `frontend/`: Next.js SaaS UI and dashboard.
- `docs/`: Architecture, API, deployment, schema, scaling.
- `.github/workflows/ci.yml`: CI pipeline template.

## Documentation Index
- `docs/project-structure.md`: full source tree.
- `docs/architecture.md`: clean architecture and service flow.
- `docs/api.md`: endpoint contracts.
- `docs/database-schema.sql`: relational schema.
- `docs/deployment.md`: local + production deployment.
- `docs/scaling.md`: 100k+ user scaling strategy.

## Scale Design (100K+ users)
- Stateless API pods with horizontal autoscaling.
- Redis caching for repeated analysis and session acceleration.
- Async workers for heavy exports and narration jobs.
- Read replicas for analytics queries.
- CDN + edge caching for frontend assets.

## License
MIT
