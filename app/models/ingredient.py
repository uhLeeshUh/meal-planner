from sqlalchemy import String
from app.models.base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped

class Ingredient(BaseModel):
    __tablename__ = "ingredients"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)