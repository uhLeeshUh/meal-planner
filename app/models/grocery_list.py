from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class GroceryList(BaseModel):
    __tablename__ = "grocery_lists"

    items = relationship("GroceryListItem", back_populates="grocery_list")