from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.meal_plan import MealPlanRequest, MealPlanResponse
from app.services.meal_plan import create_meal_plan_with_grocery_list

router = APIRouter()

@router.post("/meal-plan/generate", response_model=MealPlanResponse)
def generate_meal_plan(
    request: MealPlanRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a meal plan based on user constraints using an LLM.
    Creates recipes and optionally generates a grocery list.
    """
    try:
        meal_plan_response = create_meal_plan_with_grocery_list(
            db=db,
            request=request
        )
        return meal_plan_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating meal plan: {str(e)}")




