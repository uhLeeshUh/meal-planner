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

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Project Structure

```
meal_planner/
├── app/
│   ├── api/         # API endpoints
│   ├── core/        # Core functionality
│   ├── models/      # Database models
│   └── schemas/     # Pydantic models
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