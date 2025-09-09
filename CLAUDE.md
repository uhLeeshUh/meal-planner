# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based meal planner API with PostgreSQL backend, following a clean layered architecture pattern. The application manages meal plans, recipes, ingredients, and shopping lists.

## Tech Stack

- **Backend**: FastAPI 0.104.1 with Uvicorn server
- **Database**: PostgreSQL (SQLite fallback for development)
- **ORM**: SQLAlchemy 2.0.23 with Alembic migrations
- **Testing**: pytest with httpx for async testing
- **Containerization**: Docker + Docker Compose

## Essential Commands

### Development Server
```bash
# Start development server with auto-reload
poetry run uvicorn app.main:app --reload

# Run with Docker (full stack including database)
docker-compose up

# Database only via Docker
docker-compose up db
```

### Database Management
```bash
# Create new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Seed database with test data
python scripts/seed_db.py
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov

# Test specific file
pytest tests/repositories/test_recipes.py
```

### Code Quality
```bash
# Sort imports (only available tool currently)
isort .
```

## Architecture

The project uses a **layered architecture** with strict import hierarchy to prevent circular dependencies:

1. **Core Layer** (`app/core/`): Database connection and foundational utilities
2. **Schema Layer** (`app/schemas/`): Pydantic models for validation
3. **Model Layer** (`app/models/`): SQLAlchemy ORM models
4. **Repository Layer** (`app/repositories/`): Data access abstraction
5. **Service Layer** (`app/services/`): Business logic orchestration
6. **API Layer** (`app/api/`): FastAPI route handlers

### Import Rules
- **Core** → imports nothing
- **Schemas** → may import other schemas
- **Models** → may import other models  
- **Repositories** → imports models, schemas, core, other repositories
- **API** → imports schemas and repositories
- **Seeds/Scripts** → imports models, schemas, core, repositories

## Key Files and Directories

- `app/main.py` - FastAPI application entry point
- `app/core/database.py` - Database session management
- `migrations/` - Alembic database migrations
- `scripts/seed_db.py` - Database seeding utility
- `alembic.ini` - Migration configuration
- `.env.example` - Environment variables template
- `docker-compose.yml` - Multi-service container setup

## Database Configuration

- **Development**: SQLite (`sqlite:///./meal_planner.db`)
- **Production**: PostgreSQL via environment variable `DATABASE_URL`
- **Docker**: PostgreSQL with persistent volumes

## Development Workflow

1. **Setup**: Copy `.env.example` to `.env` and configure database settings
2. **Dependencies**: Install with `pip install -r requirements.txt`
3. **Database**: Run `alembic upgrade head` and optionally `python scripts/seed_db.py`
4. **Development**: Use `uvicorn app.main:app --reload` for hot reloading
5. **Testing**: Always run `pytest` before committing changes
6. **Migrations**: Create with `alembic revision --autogenerate` after model changes

## Current Features

- Recipe CRUD operations via REST API
- Ingredient management with units and categories
- Grocery list generation and management
- Database relationships between recipes, ingredients, and grocery lists
- Automatic API documentation at `/docs`
- Docker containerization with PostgreSQL

The application is in active development with plans for user authentication, frontend integration, and enhanced search functionality.