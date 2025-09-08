from sqlalchemy import Enum, Float, ForeignKey
from app.models.base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.schemas.enums import Unit

class RecipeIngredient(BaseModel):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=False)
    ingredient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ingredients.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Unit] = mapped_column(Enum(Unit), nullable=False)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", lazy="joined", back_populates="recipe_ingredients")