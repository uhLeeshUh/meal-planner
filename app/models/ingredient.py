from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.base_model import BaseModel

class Ingredient(BaseModel):
    __tablename__ = "ingredients"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
 

    # Relationships
    grocery_list_items = relationship("GroceryListItem", back_populates="ingredient")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")

