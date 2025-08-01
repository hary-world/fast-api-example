# Docker Deployment Documentation

## 📋 Table of Contents
1. [Dockerfile Overview](#dockerfile-overview)
2. [Environment Configuration](#environment-configuration)
3. [Docker Build Process](#docker-build-process)
4. [Docker Run Commands](#docker-run-commands)
5. [Makefile Docker Commands](#makefile-docker-commands)
6. [Database Migration in Docker](#database-migration-in-docker)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

## 🐳 Dockerfile Overview

### Current Dockerfile Analysis
```dockerfile
FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

# Copy the project files
COPY . . 

# Install the dependencies
RUN uv sync

# Expose the port
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### Key Components Explained

#### 1. **Base Image**
```dockerfile
FROM ghcr.io/astral-sh/uv:debian
```
- Uses official UV (Python package manager) image
- Based on Debian for stability
- Pre-installed with UV for fast dependency management

#### 2. **Application Setup**
```dockerfile
WORKDIR /app
COPY . .
```
- Sets working directory to `/app`
- Copies all project files into container

#### 3. **Dependency Installation**
```dockerfile
RUN uv sync
```
- Installs all dependencies from `pyproject.toml`
- Uses UV for fast, reliable dependency resolution

#### 4. **Port Configuration**
```dockerfile
EXPOSE 8000
```
- Exposes port 8000 for FastAPI application
- Maps to container's internal port

#### 5. **Application Startup**
```dockerfile
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```
- Runs database migrations first
- Starts FastAPI server with proper host binding

## ⚙️ Environment Configuration

### 1. Environment Files

#### Development Environment (`env.docker`)
```env
# Database configuration
DATABASE_URL=sqlite:///app/dev.db

# Application settings
ENVIRONMENT=development
LOG_LEVEL=debug
APP_NAME="Dependency Injection API"
APP_VERSION=1.0.0

# Server settings
HOST=0.0.0.0
PORT=8000
```

#### Production Environment (`env.prod`)
```env
# Database configuration
DATABASE_URL=sqlite:///app/prod.db

# Application settings
ENVIRONMENT=production
LOG_LEVEL=info
APP_NAME="Dependency Injection API"
APP_VERSION=1.0.0

# Server settings
HOST=0.0.0.0
PORT=8000
```

### 2. Using Environment Files

#### Docker Run with Environment File
```bash
# Run with development environment
docker run -d -p 8000:8000 --env-file env.docker haryworld/fastpi-ext

# Run with production environment
docker run -d -p 8000:8000 --env-file env.prod haryworld/fastpi-ext
```

#### Docker Compose with Environment File
```yaml
# docker-compose.yml
services:
  app:
    image: haryworld/fastpi-ext
    env_file:
      - env.docker
```

### 3. Environment Variable Override
```bash
# Override specific environment variables
docker run -d -p 8000:8000 \
  --env-file env.docker \
  -e DATABASE_URL=sqlite:///app/custom.db \
  haryworld/fastpi-ext
```

## 🔨 Docker Build Process

### 1. Build the Docker Image
```bash
# Build with default tag
docker build -t haryworld/fastpi-ext .

# Build with specific tag
docker build -t haryworld/fastpi-ext:latest .

# Build with version tag
docker build -t haryworld/fastpi-ext:v1.0.0 .
```

### 2. Build with Different Contexts
```bash
# Build from current directory
docker build -t haryworld/fastpi-ext .

# Build with specific Dockerfile
docker build -f Dockerfile -t haryworld/fastpi-ext .

# Build with no cache (force rebuild)
docker build --no-cache -t haryworld/fastpi-ext .
```

## 🚀 Docker Run Commands

### 1. Basic Run
```bash
# Run container in detached mode
docker run -d -p 8000:8000 --env-file env.docker haryworld/fastpi-ext

# Run with interactive terminal
docker run -it -p 8000:8000 --env-file env.docker haryworld/fastpi-ext

# Run with custom port mapping
docker run -d -p 3000:8000 --env-file env.docker haryworld/fastpi-ext
```

### 2. Environment Variables Override
```bash
# Override environment variables at runtime
docker run -d -p 8000:8000 \
  --env-file env.docker \
  -e ENVIRONMENT=production \
  -e DATABASE_URL=sqlite:///app/prod.db \
  haryworld/fastpi-ext
```

### 3. Volume Mounting
```bash
# Mount database file for persistence
docker run -d -p 8000:8000 \
  -v $(pwd)/dev.db:/app/dev.db \
  --env-file env.docker \
  haryworld/fastpi-ext

# Mount logs directory
docker run -d -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  --env-file env.docker \
  haryworld/fastpi-ext
```

## 🛠️ Makefile Docker Commands

### Enhanced Makefile with Environment Files
```makefile
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
```

### Usage Examples
```bash
# Build and run
make docker-build
make docker-run

# Development with volume mounting
make docker-dev

# Production deployment
make docker-prod

# View logs
make docker-logs

# Clean up
make docker-clean
```

## 🗄️ Database Migration in Docker

### 1. Migration Process
The Dockerfile automatically runs migrations on startup:
```dockerfile
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### 2. Manual Migration Commands
```bash
# Run migrations in running container
docker exec -it <container_id> uv run alembic upgrade head

# Create new migration
docker exec -it <container_id> uv run alembic revision --autogenerate -m "add new table"

# Check migration status
docker exec -it <container_id> uv run alembic current
```

### 3. Database Persistence
```bash
# Mount database file for persistence
docker run -d -p 8000:8000 \
  -v $(pwd)/dev.db:/app/dev.db \
  --env-file env.docker \
  haryworld/fastpi-ext
```

## 🚀 Production Deployment

### 1. Production Dockerfile
```dockerfile
FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

# Copy only necessary files
COPY pyproject.toml uv.lock ./
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./

# Install dependencies
RUN uv sync --frozen

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### 2. Docker Compose for Production
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: haryworld/fastpi-ext
    build: .
    ports:
      - "8000:8000"
    env_file:
      - env.prod
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 3. Production Deployment Commands
```bash
# Build and deploy
make docker-build
make docker-prod

# Or use Docker Compose
make docker-compose-up

# Check status
docker ps
make docker-logs
```

## 🔧 Troubleshooting

### 1. Common Docker Issues

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process using port
sudo kill -9 <PID>

# Or use different port
docker run -d -p 8001:8000 --env-file env.docker haryworld/fastpi-ext
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with proper user
docker run -d -p 8000:8000 \
  -u $(id -u):$(id -g) \
  --env-file env.docker \
  haryworld/fastpi-ext
```

#### Database Migration Failures
```bash
# Check migration status
docker exec -it <container_id> uv run alembic current

# Reset database
docker exec -it <container_id> rm -f dev.db
docker exec -it <container_id> uv run alembic upgrade head
```

#### Environment Variable Issues
```bash
# Check environment variables in container
docker exec -it <container_id> env

# Verify environment file is loaded
docker exec -it <container_id> cat /proc/1/environ | tr '\0' '\n'
```

### 2. Debugging Commands
```bash
# View container logs
docker logs <container_id>

# Access container shell
docker exec -it <container_id> /bin/bash

# Check container resources
docker stats <container_id>

# Inspect container
docker inspect <container_id>
```

### 3. Cleanup Commands
```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Clean up system
docker system prune -a
```

## 📋 Quick Start Guide

### 1. First Time Setup
```bash
# Build the image
make docker-build

# Run the application
make docker-run

# Check if it's running
curl http://localhost:8000/health
```

### 2. Development Workflow
```bash
# Start development environment
make docker-dev

# View logs
make docker-logs

# Stop application
make docker-stop
```

### 3. Production Deployment
```bash
# Deploy to production
make docker-prod

# Monitor application
make docker-logs

# Scale if needed
docker-compose up -d --scale app=3
```

## ⚠️ Important Notes

### 1. **Environment File Best Practices**
- Never commit sensitive environment files to version control
- Use `.env.example` as template
- Keep environment files separate for different environments
- Use `--env-file` flag for Docker commands

### 2. **Security Considerations**
- Never run containers as root in production
- Use secrets management for sensitive data
- Regularly update base images
- Scan images for vulnerabilities

### 3. **Performance Optimization**
- Use multi-stage builds for smaller images
- Implement proper health checks
- Use volume mounting for persistent data
- Configure resource limits

### 4. **Monitoring and Logging**
- Implement structured logging
- Use health check endpoints
- Monitor container resources
- Set up log aggregation

### 5. **Database Considerations**
- Use persistent volumes for database files
- Implement proper backup strategies
- Consider using external databases for production
- Test migration rollback procedures

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [Alembic Docker Guide](https://alembic.sqlalchemy.org/en/latest/cookbook.html#running-alembic-in-docker) 