from pydantic import BaseModel, Field

class IngredientBase(BaseModel):
    name: str = Field(..., description="Name of the ingredient")

class Ingredient(IngredientBase):
    id: str  # UUID will be converted to string for JSON

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model, useful in serialization from ORM -> pydantic model