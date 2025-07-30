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

# Help command
help:
	@echo "Available commands:"
	@echo "  install        - Install dependencies"
	@echo "  dev           - Start development server"
	@echo "  test          - Run tests"
	@echo "  lint          - Check code quality"
	@echo "  format        - Format and fix code"
	@echo "  init-db       - Initialize Alembic"
	@echo "  create-migration message='description' - Create new migration"
	@echo "  migrate       - Apply all migrations"
	@echo "  rollback      - Rollback last migration"
	@echo "  db-reset      - Reset database and apply migrations"
	@echo "  db-status     - Show current migration status"
	@echo "  db-history    - Show migration history"
	@echo "  init-migration - Create initial migration"
	@echo "  help          - Show this help message"

