from pydantic import BaseModel, Field
from uuid import UUID

class IngredientBase(BaseModel):
    name: str = Field(..., description="Name of the ingredient")

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: UUID  # UUID will be converted to string for JSON

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model, useful in serialization from ORM -> pydantic model