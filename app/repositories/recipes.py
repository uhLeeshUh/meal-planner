from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.schemas.recipe import Recipe as RecipeSchema, RecipeCreate
from app.repositories.ingredients import create as ingredient_create

def create_recipe(db: Session, recipe_create: RecipeCreate) -> RecipeSchema:
    # first create any new ingredients
    ingredients = []
    for ingredient in recipe_create.ingredients:
        # create ingredient db record if doesn't exist in db already
        if not hasattr(ingredient, "id") or ingredient.id is None:
            updated_ingredient = ingredient_create(db, ingredient)
        else:
            updated_ingredient = Ingredient(**ingredient.model_dump())
        ingredients.append(updated_ingredient)
    
    recipe_create.ingredients = ingredients
    
    # then create recipe
    recipe = Recipe(**recipe_create.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe

def get_recipes(db: Session, page_number: int = 0, page_size: int = 10) -> list[Recipe]:
    offset = (page_number - 1) * page_size
    return db.query(Recipe).order_by(Recipe.id).offset(offset).limit(page_size).all()