from pydantic import BaseModel
from typing import Optional

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructions: str
    prep_time: int
    cook_time: int
    servings: int

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int

    class Config:
        from_attributes = True 