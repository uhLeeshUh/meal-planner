from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.schemas.recipe import Recipe as RecipeSchema, RecipeCreate
from app.repositories.ingredients import create as ingredient_create

def create_recipe(db: Session, recipe_create: RecipeCreate) -> RecipeSchema:
    # first create any new ingredients
    ingredients = []
    for ingredient in recipe_create.ingredients:
        i = ingredient
        if not id in ingredient:
           i = ingredient_create(db, ingredient)
        ingredients.append(i)
    
    recipe_create.ingredients = ingredients
    
    # then create recipe
    recipe = Recipe(**recipe_create.dict())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe
