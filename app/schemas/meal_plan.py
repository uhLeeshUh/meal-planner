from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.recipe import Recipe, RecipeCreate

class MealPlanRequest(BaseModel):
    """Request schema for generating a meal plan"""
    num_meals: int = Field(..., description="Number of meals to generate", ge=1, le=20)
    total_time_minutes: Optional[int] = Field(None, description="Total time available for cooking all meals (in minutes)")
    preferred_ingredients: Optional[List[str]] = Field(default_factory=list, description="List of ingredients to prioritize using")
    dietary_restrictions: Optional[List[str]] = Field(default_factory=list, description="Dietary restrictions or preferences (e.g., 'vegetarian', 'gluten-free')")
    cuisine_preferences: Optional[List[str]] = Field(default_factory=list, description="Preferred cuisines (e.g., 'Italian', 'Mexican')")

class MealPlanResponse(BaseModel):
    """Response schema for a generated meal plan"""
    recipes: List[Recipe] = Field(..., description="List of generated recipes with IDs")
    grocery_list_id: Optional[str] = Field(None, description="ID of the generated grocery list (if created)")

