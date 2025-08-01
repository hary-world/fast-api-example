# Docker Deployment Documentation

## 📋 Table of Contents
1. [Dockerfile Overview](#dockerfile-overview)
2. [Environment Configuration](#environment-configuration)
3. [Docker Build Process](#docker-build-process)
4. [Docker Run Commands](#docker-run-commands)
5. [Makefile Docker Commands](#makefile-docker-commands)
6. [Docker Hub Deployment](#docker-hub-deployment)
7. [Database Migration in Docker](#database-migration-in-docker)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

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
docker run -d -p 8000:8000 --env-file env.docker haryarr/fastpi-ext

# Run with production environment
docker run -d -p 8000:8000 --env-file env.prod haryarr/fastpi-ext
```

#### Docker Compose with Environment File
```yaml
# docker-compose.yml
services:
  app:
    image: haryarr/fastpi-ext
    env_file:
      - env.docker
```

### 3. Environment Variable Override
```bash
# Override specific environment variables
docker run -d -p 8000:8000 \
  --env-file env.docker \
  -e DATABASE_URL=sqlite:///app/custom.db \
  haryarr/fastpi-ext
```

## 🔨 Docker Build Process

### 1. Build the Docker Image
```bash
# Build with default tag
docker build -t haryarr/fastpi-ext .

# Build with specific tag
docker build -t haryarr/fastpi-ext:latest .

# Build with version tag
docker build -t haryarr/fastpi-ext:v1.0.0 .
```

### 2. Build with Different Contexts
```bash
# Build from current directory
docker build -t haryarr/fastpi-ext .

# Build with specific Dockerfile
docker build -f Dockerfile -t haryarr/fastpi-ext .

# Build with no cache (force rebuild)
docker build --no-cache -t haryarr/fastpi-ext .
```

## 🚀 Docker Run Commands

### 1. Basic Run
```bash
# Run container in detached mode
docker run -d -p 8000:8000 --env-file env.docker haryarr/fastpi-ext

# Run with interactive terminal
docker run -it -p 8000:8000 --env-file env.docker haryarr/fastpi-ext

# Run with custom port mapping
docker run -d -p 3000:8000 --env-file env.docker haryarr/fastpi-ext
```

### 2. Environment Variables Override
```bash
# Override environment variables at runtime
docker run -d -p 8000:8000 \
  --env-file env.docker \
  -e ENVIRONMENT=production \
  -e DATABASE_URL=sqlite:///app/prod.db \
  haryarr/fastpi-ext
```

### 3. Volume Mounting
```bash
# Mount database file for persistence
docker run -d -p 8000:8000 \
  -v $(pwd)/dev.db:/app/dev.db \
  --env-file env.docker \
  haryarr/fastpi-ext

# Mount logs directory
docker run -d -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  --env-file env.docker \
  haryarr/fastpi-ext
```

## 🛠️ Makefile Docker Commands

### Enhanced Makefile with Environment Files
```makefile
# Docker commands
docker-build:
	docker build -t haryarr/fastpi-ext .

docker-build-dev:
	docker build -t haryarr/fastpi-ext:dev .

docker-run:
	docker run -d -p 8000:8000 --env-file env.docker haryarr/fastpi-ext

docker-stop:
	docker stop $$(docker ps -q --filter ancestor=haryarr/fastpi-ext)

docker-logs:
	docker logs $$(docker ps -q --filter ancestor=haryarr/fastpi-ext)

docker-shell:
	docker run -it haryarr/fastpi-ext /bin/bash

docker-clean:
	docker system prune -f
	docker image prune -f

# Docker development
docker-dev:
	docker run -d -p 8000:8000 \
		-v $(PWD):/app \
		-v /app/__pycache__ \
		--env-file env.docker \
		haryarr/fastpi-ext

# Docker production
docker-prod:
	docker run -d -p 8000:8000 \
		--env-file env.prod \
		haryarr/fastpi-ext

# Docker Hub commands
docker-login:
	docker login

docker-build-linux:
	docker buildx build --platform linux/amd64,linux/arm64 \
		-t haryarr/fastpi-ext:latest \
		-t haryarr/fastpi-ext:$(shell date +%Y%m%d) \
		--push .

docker-build-linux-amd64:
	docker buildx build --platform linux/amd64 \
		-t haryarr/fastpi-ext:latest \
		-t haryarr/fastpi-ext:$(shell date +%Y%m%d) \
		--push .

docker-build-linux-arm64:
	docker buildx build --platform linux/arm64 \
		-t haryarr/fastpi-ext:latest \
		-t haryarr/fastpi-ext:$(shell date +%Y%m%d) \
		--push .

docker-push:
	docker push haryarr/fastpi-ext:latest

docker-push-tag:
	docker tag haryarr/fastpi-ext:latest haryarr/fastpi-ext:$(tag)
	docker push haryarr/fastpi-ext:$(tag)

# Setup Docker Buildx for multi-platform builds
docker-setup-buildx:
	docker buildx create --name multiplatform --use
	docker buildx inspect --bootstrap

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

## 🐳 Docker Hub Deployment

### 1. Prerequisites

#### Docker Hub Account
```bash
# Create Docker Hub account at https://hub.docker.com
# Note your username for the image tag
```

#### Docker Login
```bash
# Login to Docker Hub
make docker-login
# Enter your Docker Hub username and password
```

### 2. Multi-Platform Build Setup

#### Setup Docker Buildx
```bash
# Setup multi-platform build capability
make docker-setup-buildx

# Verify buildx is working
docker buildx ls
```

#### Available Platforms
```bash
# Linux AMD64 (Intel/AMD processors)
make docker-build-linux-amd64

# Linux ARM64 (Apple Silicon, ARM servers)
make docker-build-linux-arm64

# Both platforms (recommended)
make docker-build-linux
```

### 3. Build and Push Commands

#### Build for Linux AMD64
```bash
# Build and push for Linux AMD64
make docker-build-linux-amd64

# This creates:
# - haryarr/fastpi-ext:latest (AMD64)
# - haryarr/fastpi-ext:YYYYMMDD (AMD64)
```

#### Build for Linux ARM64
```bash
# Build and push for Linux ARM64
make docker-build-linux-arm64

# This creates:
# - haryarr/fastpi-ext:latest (ARM64)
# - haryarr/fastpi-ext:YYYYMMDD (ARM64)
```

#### Build for Multiple Platforms
```bash
# Build and push for both AMD64 and ARM64
make docker-build-linux

# This creates multi-platform images:
# - haryarr/fastpi-ext:latest (AMD64 + ARM64)
# - haryarr/fastpi-ext:YYYYMMDD (AMD64 + ARM64)
```

### 4. Manual Push Commands

#### Push Latest Image
```bash
# Build locally first
make docker-build

# Push to Docker Hub
make docker-push
```

#### Push Tagged Image
```bash
# Build locally
make docker-build

# Push with specific tag
make docker-push-tag tag=v1.0.0
```

### 5. Pull and Run from Docker Hub

#### Pull Image
```bash
# Pull latest image
docker pull haryarr/fastpi-ext:latest

# Pull specific version
docker pull haryarr/fastpi-ext:v1.0.0
```

#### Run from Docker Hub
```bash
# Run latest image
docker run -d -p 8000:8000 \
  --env-file env.docker \
  haryarr/fastpi-ext:latest

# Run specific version
docker run -d -p 8000:8000 \
  --env-file env.prod \
  haryarr/fastpi-ext:v1.0.0
```

### 6. Platform-Specific Commands

#### Check Image Architecture
```bash
# Check image platform
docker image inspect haryarr/fastpi-ext:latest | grep Architecture

# List all platforms for multi-platform image
docker manifest inspect haryarr/fastpi-ext:latest
```

#### Run on Specific Platform
```bash
# Force run on AMD64
docker run --platform linux/amd64 haryarr/fastpi-ext:latest

# Force run on ARM64
docker run --platform linux/arm64 haryarr/fastpi-ext:latest
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
  haryarr/fastpi-ext
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
    image: haryarr/fastpi-ext
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
docker run -d -p 8001:8000 --env-file env.docker haryarr/fastpi-ext
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with proper user
docker run -d -p 8000:8000 \
  -u $(id -u):$(id -g) \
  --env-file env.docker \
  haryarr/fastpi-ext
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

### 2. Docker Hub Issues

#### Buildx Not Available
```bash
# Setup buildx
make docker-setup-buildx

# Check available builders
docker buildx ls

# Create new builder if needed
docker buildx create --name multiplatform --driver docker-container
```

#### Authentication Issues
```bash
# Re-login to Docker Hub
docker logout
make docker-login

# Check login status
docker info | grep Username
```

#### Platform Build Failures
```bash
# Check available platforms
docker buildx inspect --bootstrap

# Build for specific platform only
make docker-build-linux-amd64

# Check image architecture
docker image inspect haryarr/fastpi-ext:latest | grep Architecture
```

### 3. Debugging Commands
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

### 4. Cleanup Commands
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

### 4. Docker Hub Deployment
```bash
# Login to Docker Hub
make docker-login

# Setup multi-platform build
make docker-setup-buildx

# Build and push for Linux
make docker-build-linux

# Pull and run from Docker Hub
docker pull haryarr/fastpi-ext:latest
docker run -d -p 8000:8000 --env-file env.docker haryarr/fastpi-ext:latest
```

## ⚠️ Important Notes

### 1. **Environment File Best Practices**
- Never commit sensitive environment files to version control
- Use `.env.example` as template
- Keep environment files separate for different environments
- Use `--env-file` flag for Docker commands

### 2. **Docker Hub Best Practices**
- Use semantic versioning for tags
- Include date tags for traceability
- Build multi-platform images for wider compatibility
- Test images on different platforms before pushing

### 3. **Security Considerations**
- Never run containers as root in production
- Use secrets management for sensitive data
- Regularly update base images
- Scan images for vulnerabilities

### 4. **Performance Optimization**
- Use multi-stage builds for smaller images
- Implement proper health checks
- Use volume mounting for persistent data
- Configure resource limits

### 5. **Monitoring and Logging**
- Implement structured logging
- Use health check endpoints
- Monitor container resources
- Set up log aggregation

### 6. **Database Considerations**
- Use persistent volumes for database files
- Implement proper backup strategies
- Consider using external databases for production
- Test migration rollback procedures

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Docker Buildx Documentation](https://docs.docker.com/buildx/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [Alembic Docker Guide](https://alembic.sqlalchemy.org/en/latest/cookbook.html#running-alembic-in-docker) 