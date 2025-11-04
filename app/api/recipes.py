from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.recipe import Recipe as RecipeModel
from app.schemas.recipe import Recipe, RecipeCreate, ScrapeRecipeRequest
from app.repositories.recipes import get_recipes as get_recipes_repo, get_recipe as get_recipe_repo, create_recipe as create_recipe_repo
from app.services.recipe import scrape_recipe as scrape_recipe_service

router = APIRouter()

@router.get("/recipes/", response_model=List[Recipe])
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = get_recipes_repo(db, page_number=skip, page_size=limit)
    return recipes

@router.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = create_recipe_repo(db, recipe)
    return db_recipe

@router.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: UUID, db: Session = Depends(get_db)):
    recipe = get_recipe_repo(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe 

@router.post("/recipes/scrape")
def scrape_recipe(request: ScrapeRecipeRequest):
    recipe = scrape_recipe_service(request.url)
    return recipe