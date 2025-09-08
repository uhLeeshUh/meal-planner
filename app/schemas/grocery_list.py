from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.enums import Unit
from typing import List
from app.schemas.ingredient import Ingredient

#GroceryListItem
class GroceryListItemBase(BaseModel):
    grocery_list_id: UUID = Field(..., description="Foreign key id of grocery_list")
    ingredient_id: UUID = Field(..., description="Foreign key id of ingredient")
    quantity: float = Field(..., description="Amount of the ingredient")
    unit: Unit = Field(..., description="Unit of the ingredient")

class GroceryListItem(GroceryListItemBase):
    id: UUID  # UUID will be converted to string for JSON

    ingredient: Ingredient

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model 

class IngredientListItem(BaseModel):
    ingredient_id: UUID = Field(..., description="ID of the ingredient")
    total_quantity: float = Field(..., description="Amount of the ingredient")
    unit: Unit = Field(..., description="Unit of the ingredient")

class GroceryListCreate(BaseModel):
    items: List[IngredientListItem]

# GroceryList
class GroceryListBase(BaseModel):
    pass

class GroceryList(GroceryListBase):
    id: UUID  # UUID will be converted to string for JSON
    items: List[GroceryListItem] | None = Field(None, description="Ingredients with quantities")

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model 
