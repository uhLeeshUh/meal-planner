from pydantic import BaseModel, Field
from typing import Optional

class RecipeBase(BaseModel):
    name: str = Field(..., description="Name of the recipe")
    prep_instructions: Optional[str] = Field(None, description="Preparation instructions")
    cooking_instructions: str = Field(..., description="Cooking instructions")
    prep_time: Optional[int] = Field(None, description="Preparation time in minutes")
    cook_time: int = Field(..., description="Cooking time in minutes")
    servings: Optional[int] = Field(None, description="Number of servings")
    image_url: Optional[str] = Field(None, description="URL to recipe image")

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: str  # UUID will be converted to string for JSON

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model 