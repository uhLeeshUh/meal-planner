# Meal Planner API

A FastAPI-based meal planning application that helps users manage their meal plans, recipes, and shopping lists.

## Features

- Create and manage meal plans
- Store and retrieve recipes
- Generate shopping lists
- RESTful API endpoints
- Postgres database (can be configured for other databases)

## Setup

1. Create a virtual environment, using poetry (if you don't have poetry globally installed, do so first):
```bash
poetry env activate
```

2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start up the postgres docker container
```bash
docker-compose up db
```

5. Run the application:
```bash
poetry run uvicorn app.main:app --reload
```

For migrating the database:
1. From project root, run a migration after making data model changes:
```bash
poetry run alembic revision --autogenerate -m "description of your changes"
```
2. Apply the change
```bash
poetry run alembic upgrade head
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Development notes

The python virtual env is managed by Poetry. 

To add new dependencies, use the `poetry add <package>` command. 

To run commands in the Poetry environment, use `poetry run <command>`

## Project Structure

```
meal_planner/
├── app/
│   ├── api/         # API endpoints
│   ├── core/        # Core functionality (db setup)
│   ├── models/      # Database models
│   └── repositories/# Direct callers of the database
│   └── schemas/     # Pydantic DTOs. Validation models for request/response or inter-layer contracts
│   └── seeds/       # Db seed data
    └── services/    # Business logic 
├── migrations/      # Db migrations, managed by alembic
├── scripts/         # App-wide scripts
├── tests/           # Test files
├── requirements.txt # Project dependencies
└── README.md       # This file
```

## Testing

Run tests with:
```bash
pytest
```

## One-off Testing

This project has ipython installed, which is an interactive python shell that lets you play around
with code you've written. 

To test functions one-off as you're building them, this can be preferred to writing a unit test.

To do so, instantiate an ipython shell at the command line with `ipython`

Now in your REPL, you can do things like interact with the db:

```
from app.core.database import get_db

db = next(get_db())

from app.repositories.ingredients import get_by_name

get_by_name(db, "lemon")
```

## License

MIT 