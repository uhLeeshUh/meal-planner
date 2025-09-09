from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.core.database import get_db
from app.models.recipe import Recipe as RecipeModel
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe import Recipe, RecipeCreate
from app.repositories.recipes import get_recipes as get_recipes_repo

router = APIRouter()

@router.get("/recipes/", response_model=List[Recipe])
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = get_recipes_repo(db, page_number=skip, page_size=limit)
    return recipes

@router.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = RecipeModel(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: UUID, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe 