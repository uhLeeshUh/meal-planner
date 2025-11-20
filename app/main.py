from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import recipes, grocery_list, meal_plan

app = FastAPI(
    title="Meal Planner API",
    description="API for managing meal plans and recipes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recipes.router, tags=["recipes"])
app.include_router(grocery_list.router, tags=["grocery-lists"])
app.include_router(meal_plan.router, tags=["meal-plan"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Meal Planner API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 