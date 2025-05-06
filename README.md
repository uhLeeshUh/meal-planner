# Meal Planner API

A FastAPI-based meal planning application that helps users manage their meal plans, recipes, and shopping lists.

## Features

- Create and manage meal plans
- Store and retrieve recipes
- Generate shopping lists
- RESTful API endpoints
- SQLite database (can be configured for other databases)

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
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
uvicorn app.main:app --reload
```

For migrating the database:
1. From project root, run a migration after making data model changes:
```bash
alembic revision --autogenerate -m "description of your changes"
```
2. Apply the change
```bash
alembic upgrade head
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Project Structure

```
meal_planner/
├── app/
│   ├── api/         # API endpoints
│   ├── core/        # Core functionality (db setup)
│   ├── models/      # Database models
│   └── repositories/# Business logic to interact with database
│   └── schemas/     # Pydantic models for validation
│   └── seeds/       # Db seed data
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

## License

MIT 