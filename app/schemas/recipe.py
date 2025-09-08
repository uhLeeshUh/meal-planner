from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

from app.schemas.recipe_ingredient import RecipeIngredient
from app.schemas.enums import Unit

class RecipeIngredientCreate(BaseModel):
    """Schema for creating an ingredient with quantity and unit for a recipe"""
    name: str = Field(..., description="Name of the ingredient")
    quantity: float = Field(..., description="Amount of the ingredient")
    unit: Unit = Field(..., description="Unit of the ingredient")

class RecipeBase(BaseModel):
    name: str = Field(..., description="Name of the recipe")
    prep_instructions: str | None = Field(None, description="Preparation instructions")
    cooking_instructions: str = Field(..., description="Cooking instructions")
    prep_time: int | None = Field(None, description="Preparation time in minutes")
    cook_time: int = Field(..., description="Cooking time in minutes")
    servings: int | None = Field(None, description="Number of servings")
    image_url: str | None = Field(None, description="URL to recipe image")

class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] # ingredients with quantities and units for the recipe

class Recipe(RecipeBase):
    id: UUID
    recipe_ingredients: List[RecipeIngredient] = []

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model 