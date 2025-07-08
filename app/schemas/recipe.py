from pydantic import BaseModel, Field
from typing import List

from app.schemas.ingredient import Ingredient, IngredientCreate
from app.schemas.recipe_ingredient import RecipeIngredient

class RecipeBase(BaseModel):
    name: str = Field(..., description="Name of the recipe")
    prep_instructions: str | None = Field(None, description="Preparation instructions")
    cooking_instructions: str = Field(..., description="Cooking instructions")
    prep_time: int | None = Field(None, description="Preparation time in minutes")
    cook_time: int = Field(..., description="Cooking time in minutes")
    servings: int | None = Field(None, description="Number of servings")
    image_url: str | None = Field(None, description="URL to recipe image")

class RecipeCreate(RecipeBase):
    ingredients: List[Ingredient | IngredientCreate] # allow new ingredients to be created alongside their respective recipes

class Recipe(RecipeBase):
    id: str  # UUID will be converted to string for JSON
    recipe_ingredients: List[RecipeIngredient]

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model 