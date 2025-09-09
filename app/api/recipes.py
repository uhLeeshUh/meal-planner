from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.core.database import get_db
from app.models.recipe import Recipe as RecipeModel
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe import Recipe, RecipeCreate

router = APIRouter()

@router.get("/recipes/", response_model=List[Recipe])
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = (
        db.query(RecipeModel)
        .options(
            joinedload(RecipeModel.recipe_ingredients)
            .joinedload(RecipeIngredient.ingredient)
        )
        .order_by(RecipeModel.name)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Sort ingredients within each recipe alphabetically
    for recipe in recipes:
        recipe.recipe_ingredients.sort(key=lambda ri: ri.ingredient.name.lower())
    
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