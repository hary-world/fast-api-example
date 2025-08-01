# Development commands
install:
	uv sync

dev: 
	uv run uvicorn app.main:app --reload

test:
	uv run pytest

# Code quality
lint:
	uv run ruff check

format:
	uv run ruff format
	uv run ruff check --fix

# Database commands
init-db:
	uv run alembic init migrations

create-migration:
	uv run alembic revision --autogenerate -m "$(message)"

migrate:
	uv run alembic upgrade head

rollback:
	uv run alembic downgrade -1

# Database management
db-reset:
	rm -f dev.db
	uv run alembic upgrade head

# Show database status
db-status:
	uv run alembic current
	uv run alembic history

# Show migration history
db-history:
	uv run alembic history --verbose

# Create initial migration (if no migrations exist)
init-migration:
	uv run alembic revision --autogenerate -m "initial setup"

# Docker commands
docker-build:
	docker build -t haryworld/fastpi-ext .

docker-build-dev:
	docker build -t haryworld/fastpi-ext:dev .

docker-run:
	docker run -d -p 8000:8000 --env-file env.docker haryworld/fastpi-ext

docker-stop:
	docker stop $$(docker ps -q --filter ancestor=haryworld/fastpi-ext)

docker-logs:
	docker logs $$(docker ps -q --filter ancestor=haryworld/fastpi-ext)

docker-shell:
	docker run -it haryworld/fastpi-ext /bin/bash

docker-clean:
	docker system prune -f
	docker image prune -f

# Docker development
docker-dev:
	docker run -d -p 8000:8000 \
		-v $(PWD):/app \
		-v /app/__pycache__ \
		--env-file env.docker \
		haryworld/fastpi-ext

# Docker production
docker-prod:
	docker run -d -p 8000:8000 \
		--env-file env.prod \
		haryworld/fastpi-ext

# Docker compose
docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

docker-compose-logs:
	docker-compose logs -f

# Help command
help:
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  install        - Install dependencies"
	@echo "  dev           - Start development server"
	@echo "  test          - Run tests"
	@echo "  lint          - Check code quality"
	@echo "  format        - Format and fix code"
	@echo ""
	@echo "Database:"
	@echo "  init-db       - Initialize Alembic"
	@echo "  create-migration message='description' - Create new migration"
	@echo "  migrate       - Apply all migrations"
	@echo "  rollback      - Rollback last migration"
	@echo "  db-reset      - Reset database and apply migrations"
	@echo "  db-status     - Show current migration status"
	@echo "  db-history    - Show migration history"
	@echo "  init-migration - Create initial migration"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-build-dev - Build development Docker image"
	@echo "  docker-run    - Run Docker container with env.docker"
	@echo "  docker-stop   - Stop Docker container"
	@echo "  docker-logs   - View Docker logs"
	@echo "  docker-shell  - Access Docker container shell"
	@echo "  docker-clean  - Clean Docker system"
	@echo "  docker-dev    - Run Docker in development mode"
	@echo "  docker-prod   - Run Docker in production mode"
	@echo "  docker-compose-up   - Start with Docker Compose"
	@echo "  docker-compose-down  - Stop Docker Compose"
	@echo "  docker-compose-logs  - View Docker Compose logs"
	@echo ""
	@echo "  help          - Show this help message"

