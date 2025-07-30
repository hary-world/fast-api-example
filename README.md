# Dependency Injection Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Dependencies](#dependencies)
3. [Environment Setup](#environment-setup)
4. [Database Configuration](#database-configuration)
5. [Alembic Migration Setup](#alembic-migration-setup)
6. [Makefile Commands](#makefile-commands)
7. [Project Structure](#project-structure)
8. [Key Concepts](#key-concepts)

## 🎯 Project Overview

This is a FastAPI-based project with SQLModel for database models, Alembic for migrations, and dependency injection patterns. The project demonstrates a clean architecture with proper separation of concerns.

## 📦 Dependencies

### Core Dependencies
```toml
[project]
dependencies = [
    "alembic>=1.16.4",        # Database migration tool
    "fastapi[standard]>=0.116.1",  # Web framework
    "python-dotenv>=1.1.1",    # Environment variable management
    "ruff>=0.12.7",           # Code formatting and linting
    "scalar-fastapi>=1.2.2",   # API documentation
    "sqlmodel>=0.0.24",       # SQL database ORM
    "uvicorn>=0.35.0",        # ASGI server
    "email-validator>=2.2.0",  # Email validation
]
```

### Key Dependencies Explained

#### 1. **SQLModel**
- Combines SQLAlchemy and Pydantic
- Provides type-safe database models
- Automatic schema generation

#### 2. **Alembic**
- Database migration tool for SQLAlchemy
- Handles schema changes and version control
- Supports both online and offline migrations

#### 3. **python-dotenv**
- Loads environment variables from `.env` files
- Essential for configuration management
- Used with `load_dotenv(override=True)`

#### 4. **Ruff**
- Fast Python linter and formatter
- Replaces multiple tools (black, isort, flake8)
- Configured in `pyproject.toml`

## 🔧 Environment Setup

### 1. Load Environment Variables
```python
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)
```

### 2. Database URL Configuration
```python
# In migrations/env.py
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

### 3. Alembic Configuration
```ini
# In alembic.ini
sqlalchemy.url = 
```

**Important**: The `sqlalchemy.url` in `alembic.ini` should be empty because it's overridden in `env.py` using environment variables.

## 🗄️ Database Configuration

### SQLModel Setup
```python
from sqlmodel import SQLModel, Field

class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    is_completed: bool = Field(default=False)
```

### Database Models Pattern
```python
# Base model for creation
class NoteCreate(SQLModel):
    text: str

# Base model for reading
class NoteRead(SQLModel):
    id: int
    text: str
```

## 🔄 Alembic Migration Setup

### 1. Environment Configuration (`migrations/env.py`)
```python
import os
from logging.config import fileConfig
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from app.database import Note  # Import your models

load_dotenv(override=True)

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
target_metadata = SQLModel.metadata
```

### 2. Key Configuration Points
- **Model Imports**: Import all models in `env.py` for autogenerate
- **Metadata**: Use `SQLModel.metadata` as target metadata
- **Database URL**: Override from environment variables

## 🛠️ Makefile Commands

### Current Makefile
```makefile
format:
	uv run ruff format
	uv run ruff check --fix

dev: 
	uv run uvicorn app.main:app --reload
```

### Recommended Additional Commands
```makefile
# Database commands
init-db:
	uv run alembic init migrations

create-migration:
	uv run alembic revision --autogenerate -m "$(message)"

migrate:
	uv run alembic upgrade head

rollback:
	uv run alembic downgrade -1

# Development commands
install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check

format:
	uv run ruff format
	uv run ruff check --fix

dev:
	uv run uvicorn app.main:app --reload

# Database management
db-reset:
	rm -f dev.db
	uv run alembic upgrade head
```

## 📁 Project Structure

```
dependency-injection/
├── alembic.ini              # Alembic configuration
├── app/
│   ├── __init__.py
│   ├── database.py          # SQLModel models
│   ├── main.py             # FastAPI application
│   ├── schema.py           # Pydantic schemas
│   └── settings.py         # Application settings
├── migrations/
│   ├── env.py              # Alembic environment
│   ├── script.py.mako      # Migration template
│   └── versions/           # Migration files
├── dev.db                  # SQLite database
├── Makefile                # Build commands
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
└── README.md
```

## 🔑 Key Concepts

### 1. **Dependency Injection Pattern**
- Services are injected into endpoints
- Clean separation of concerns
- Easy testing and mocking

### 2. **Environment Variable Management**
```python
# Always use override=True for development
load_dotenv(override=True)

# Access environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
```

### 3. **Database Migration Workflow**
```bash
# 1. Create a new migration
make create-migration message="add user table"

# 2. Apply migrations
make migrate

# 3. Rollback if needed
make rollback
```

### 4. **Code Quality Tools**
```bash
# Format and lint code
make format

# Check for issues
make lint

# Run tests
make test
```

## 🚀 Quick Start Commands

### Initial Setup
```bash
# Install dependencies
make install

# Initialize database
make init-db

# Create first migration
make create-migration message="initial setup"

# Apply migrations
make migrate

# Start development server
make dev
```

### Development Workflow
```bash
# 1. Make code changes
# 2. Format code
make format

# 3. Create migration for model changes
make create-migration message="add new feature"

# 4. Apply migration
make migrate

# 5. Test changes
make test

# 6. Start server
make dev
```

## ⚠️ Important Notes

### 1. **Environment Variables**
- Always use `.env` file for sensitive data
- Never commit `.env` files to version control
- Use `load_dotenv(override=True)` for development

### 2. **Database Migrations**
- Always create migrations for schema changes
- Test migrations in development before production
- Use descriptive migration messages

### 3. **Code Quality**
- Run `make format` before committing
- Use `make lint` to check for issues
- Follow the established project structure

### 4. **Alembic Configuration**
- Keep `sqlalchemy.url = ""` in `alembic.ini`
- Override URL in `env.py` using environment variables
- Import all models in `env.py` for autogenerate

## 🔧 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   # Reset database
   make db-reset
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   make install
   ```

3. **Format Issues**
   ```bash
   # Format code
   make format
   ```

## 📚 Additional Resources

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/) 