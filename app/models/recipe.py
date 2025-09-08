from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.base_model import BaseModel

class Recipe(BaseModel):
    __tablename__ = "recipes"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    prep_instructions: Mapped[str | None] = mapped_column(Text)
    cooking_instructions: Mapped[str] = mapped_column(Text, nullable=False)
    prep_time: Mapped[int | None] = mapped_column(Integer)  # in minutes
    cook_time: Mapped[int] = mapped_column(Integer, nullable=False)  # in minutes
    servings: Mapped[int | None] = mapped_column(Integer)
    image_url: Mapped[str | None] = mapped_column(String)
    
    # Relationships
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe", lazy="joined")