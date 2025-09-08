from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.recipes import get_ingredients_list_for_recipes
from app.repositories.grocery_list import create_grocery_list
from app.schemas.grocery_list import GroceryListCreate

def build_grocery_list(db: Session, recipe_ids: list[UUID]):
    # load all recipe_ingredients from the list of recipe_ids (recipe repo)
    # (AU TODO) maybe move this in memory to handle discrepancies in units 
    # (e.g. combining teaspoons and tablespoons)
    ingredients_list = get_ingredients_list_for_recipes(db, recipe_ids)

    # create grocery list with correct ingredient quantities (repo)
    grocery_list = create_grocery_list(db, GroceryListCreate(items=ingredients_list))
    
    # return grocery list with eager loaded ingredients ordered alphabetically
    # (AU TODO) - eventually would be nice to order these primarily by type, e.g. produce, dairy, etc
    return grocery_list