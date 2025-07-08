from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate
import uuid

def get_by_id(db: Session, id: uuid.UUID) -> Ingredient | None:
    return db.query(Ingredient).filter(Ingredient.id == id).first()

def get_by_name(db: Session, name: str) -> list[Ingredient] | None:
    return db.query(Ingredient).filter(Ingredient.name.ilike(f"%{name}%")).all()

def create(db: Session, ingredient_create: IngredientCreate) -> Ingredient:
    ingredient = Ingredient(**ingredient_create.dict())
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient