from sqlalchemy import String, Float, ForeignKey
from app.models.base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class GroceryListItem(BaseModel):
    __tablename__ = "grocery_list_items"

    grocery_list_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("grocery_lists.id"), nullable=False)
    ingredient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ingredients.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False) # use American standard units, eg. cups, tablespoons, teaspoons, etc.

    grocery_list = relationship("GroceryList", back_populates="items")
    ingredient = relationship("Ingredient", back_populates="grocery_list_items", lazy='joined', order_by="Ingredient.name")