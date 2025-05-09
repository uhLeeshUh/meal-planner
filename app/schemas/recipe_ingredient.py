from pydantic import BaseModel, Field
from app.schemas.enums import Unit

class RecipeIngredientBase(BaseModel):
    recipe_id: str = Field(..., description="Foreign key id of recipe")
    ingredient_id: str = Field(..., description="Foreign key id of ingredient")
    quantity: float = Field(..., description="Amount of the ingredient")
    unit: Unit = Field(..., description="Unit of the ingredient")

class RecipeIngredient(RecipeIngredientBase):
    id: str  # UUID will be converted to string for JSON

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model 