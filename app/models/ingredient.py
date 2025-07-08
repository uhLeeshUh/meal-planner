from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.base_model import BaseModel

class Ingredient(BaseModel):
    __tablename__ = "ingredients"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
 

    # Relationships
    recipes = relationship(
        "Recipe",
        secondary="recipe_ingredients",
        back_populates="ingredients"
    )


