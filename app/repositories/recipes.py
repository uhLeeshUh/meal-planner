from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from collections import Counter

from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe import Recipe as RecipeSchema, RecipeCreate
from app.schemas.grocery_list import IngredientListItem

def sort_recipe_ingredients_alpha(recipe: Recipe) -> None:
    """
    Sort a recipe's recipe_ingredients list by Ingredient.name (case-insensitive).
    Mutates the passed-in recipe.
    """
    if recipe and getattr(recipe, 'recipe_ingredients', None):
        recipe.recipe_ingredients.sort(key=lambda ri: ri.ingredient.name.lower())

def create_recipe(db: Session, recipe_create: RecipeCreate) -> RecipeSchema:
    # Create the recipe first (without ingredients)
    recipe_data = recipe_create.model_dump(exclude={'ingredients'})
    recipe = Recipe(**recipe_data)
    db.add(recipe)
    db.flush()  # Get the recipe ID
    
    # Create ingredients and recipe_ingredient relationships
    for ingredient_data in recipe_create.ingredients:
        # Check if ingredient already exists by ID first, then by name
        if hasattr(ingredient_data, 'id') and ingredient_data.id:
            existing_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_data.id).first()
        else:
            existing_ingredient = db.query(Ingredient).filter(func.lower(Ingredient.name) == func.lower(ingredient_data.name)).first()
        
        if existing_ingredient:
            ingredient = existing_ingredient
        else:
            # Create new ingredient
            ingredient = Ingredient(name=ingredient_data.name)
            db.add(ingredient)
            db.flush()  # Get the ingredient ID
        
        # Create recipe_ingredient relationship with quantity and unit
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=ingredient_data.quantity,
            unit=ingredient_data.unit
        )
        db.add(recipe_ingredient)
    
    db.commit()
    db.refresh(recipe)
    
    return recipe

def get_recipes(db: Session, page_number: int = 0, page_size: int = 10) -> list[Recipe]:
    offset = page_number * page_size
    recipes = (
        db.query(Recipe)
        .options(
            joinedload(Recipe.recipe_ingredients)
            .joinedload(RecipeIngredient.ingredient)
        )
        .order_by(Recipe.name)
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    # Sort recipe_ingredients by ingredient name for each recipe
    # This is still efficient since we're sorting small lists (typically < 20 items)
    for recipe in recipes:
        sort_recipe_ingredients_alpha(recipe)
    
    return recipes

"""
Fetch a single recipe with its ingredients eagerly loaded and sort
the ingredients by name in Python. SQLAlchemy does not support ordering
by Ingredient.name in the SQL layer, so we do it in Python.
"""
def get_recipe(db: Session, recipe_id: UUID) -> Recipe:
    recipe = (
        db.query(Recipe)
        .options(
            joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)
        )
        .filter(Recipe.id == recipe_id)
        .first()
    )
    if recipe:
        sort_recipe_ingredients_alpha(recipe)
    return recipe

def get_ingredients_list_for_recipes(db: Session, recipe_ids: list[UUID]) -> list[IngredientListItem]:
    """
    Get aggregated ingredients for a list of recipes.
    Handles duplicate recipe IDs by counting occurrences and multiplying quantities.
    Returns a list of dictionaries with ingredient name, total quantity, and unit.
    """
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient
    from app.models.recipe_ingredient import RecipeIngredient
    
    # Count how many times each recipe_id appears (for multipliers)
    recipe_counts = Counter(recipe_ids)
    unique_recipe_ids = list(recipe_counts.keys())
    
    # Query RecipeIngredient rows for the unique recipe IDs
    recipe_ingredients = db.query(
        RecipeIngredient.recipe_id,
        RecipeIngredient.ingredient_id,
        RecipeIngredient.quantity,
        RecipeIngredient.unit
    ).join(
        Recipe, RecipeIngredient.recipe_id == Recipe.id
    ).filter(
        Recipe.id.in_(unique_recipe_ids)
    ).all()
    
    # Aggregate quantities, multiplying by the count of each recipe_id
    aggregated = {}
    for ri in recipe_ingredients:
        multiplier = recipe_counts[ri.recipe_id]
        key = (ri.ingredient_id, ri.unit)
        
        if key not in aggregated:
            aggregated[key] = 0
        aggregated[key] += ri.quantity * multiplier
    
    # Convert to list of dictionaries
    return [
        {
            'ingredient_id': ingredient_id,
            'total_quantity': total_quantity,
            'unit': unit
        }
        for (ingredient_id, unit), total_quantity in aggregated.items()
    ]