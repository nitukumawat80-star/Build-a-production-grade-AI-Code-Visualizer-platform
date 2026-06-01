# Project Structure

```text
.
|-- .env.example
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- backend/
|   |-- .dockerignore
|   |-- Dockerfile
|   |-- app/
|   |   |-- api/
|   |   |   `-- v1/
|   |   |       |-- router.py
|   |   |       `-- routes/
|   |   |           |-- analysis.py
|   |   |           |-- dashboard.py
|   |   |           |-- exports.py
|   |   |           `-- health.py
|   |   |-- application/
|   |   |   `-- services/
|   |   |       |-- analysis_service.py
|   |   |       |-- bug_service.py
|   |   |       |-- complexity_service.py
|   |   |       |-- export_service.py
|   |   |       |-- narration_service.py
|   |   |       |-- optimization_service.py
|   |   |       |-- pattern_service.py
|   |   |       `-- smell_service.py
|   |   |-- core/
|   |   |   |-- config.py
|   |   |   `-- logging.py
|   |   |-- db/
|   |   |   |-- base.py
|   |   |   |-- models.py
|   |   |   `-- session.py
|   |   |-- domain/
|   |   |   |-- entities/
|   |   |   |   `-- analysis.py
|   |   |   `-- interfaces/
|   |   |       |-- ast_parser.py
|   |   |       `-- repositories.py
|   |   |-- infrastructure/
|   |   |   |-- ast/
|   |   |   |   |-- parser_factory.py
|   |   |   |   |-- python_parser.py
|   |   |   |   |-- tree_sitter_parser.py
|   |   |   |   `-- runtime/
|   |   |   |       `-- python_dry_run.py
|   |   |   |-- cache/
|   |   |   |   `-- redis_cache.py
|   |   |   `-- repositories/
|   |   |       |-- analysis_repository.py
|   |   |       `-- user_repository.py
|   |   |-- schemas/
|   |   |   |-- analysis.py
|   |   |   |-- dashboard.py
|   |   |   `-- export.py
|   |   |-- workers/
|   |   |   `-- export_worker.py
|   |   `-- main.py
|   |-- requirements.txt
|   `-- tests/
|       |-- integration/test_analysis_api.py
|       `-- unit/
|           |-- test_complexity_service.py
|           `-- test_pattern_service.py
|-- docs/
|   |-- api.md
|   |-- architecture.md
|   |-- database-schema.sql
|   |-- deployment.md
|   |-- project-structure.md
|   `-- scaling.md
|-- docker-compose.yml
|-- frontend/
|   |-- Dockerfile
|   |-- app/
|   |   |-- dashboard/page.tsx
|   |   |-- globals.css
|   |   |-- layout.tsx
|   |   `-- page.tsx
|   |-- components/
|   |   |-- DropZone.tsx
|   |   |-- ExportBar.tsx
|   |   |-- InsightsPanel.tsx
|   |   |-- MemoryAndStackPanel.tsx
|   |   |-- MonacoEditorPanel.tsx
|   |   |-- NarrationPanel.tsx
|   |   |-- TimelinePlayer.tsx
|   |   `-- VisualizerShell.tsx
|   |-- lib/
|   |   |-- api.ts
|   |   `-- types.ts
|   |-- package.json
|   |-- package-lock.json
|   |-- .dockerignore
|   |-- postcss.config.js
|   |-- tailwind.config.ts
|   `-- tsconfig.json
|-- Makefile
`-- README.md
```
