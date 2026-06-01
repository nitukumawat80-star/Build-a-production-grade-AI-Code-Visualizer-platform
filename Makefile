.PHONY: dev up down backend-test frontend-test lint format

dev:
	docker compose up --build

up:
	docker compose up -d --build

down:
	docker compose down

backend-test:
	cd backend && pytest -q

frontend-test:
	cd frontend && npm run test

lint:
	cd backend && ruff check app tests
	cd frontend && npm run lint

format:
	cd backend && ruff format app tests
	cd frontend && npm run format
