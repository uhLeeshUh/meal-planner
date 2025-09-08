from pydantic import BaseModel, Field
from app.schemas.enums import Unit
from app.schemas.ingredient import Ingredient
from uuid import UUID

class RecipeIngredientBase(BaseModel):
    recipe_id: UUID = Field(..., description="Foreign key id of recipe")
    ingredient_id: UUID = Field(..., description="Foreign key id of ingredient")
    quantity: float = Field(..., description="Amount of the ingredient")
    unit: Unit = Field(..., description="Unit of the ingredient")

class RecipeIngredient(RecipeIngredientBase):
    id: UUID  # UUID will be converted to string for JSON
    ingredient: Ingredient

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model 