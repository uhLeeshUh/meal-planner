from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe import Recipe as RecipeSchema, RecipeCreate
from app.schemas.grocery_list import IngredientListItem

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
    offset = (page_number - 1) * page_size
    return db.query(Recipe).order_by(Recipe.id).offset(offset).limit(page_size).all()

def get_ingredients_list_for_recipes(db: Session, recipe_ids: list[UUID]) -> list[IngredientListItem]:
    """
    Get aggregated ingredients for a list of recipes.
    Returns a list of dictionaries with ingredient name, total quantity, and unit.
    """
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient
    from app.models.recipe_ingredient import RecipeIngredient
    
    result = db.query(
        Ingredient.id,
        func.sum(RecipeIngredient.quantity).label('total_quantity'),
        RecipeIngredient.unit
    ).join(
        RecipeIngredient, Ingredient.id == RecipeIngredient.ingredient_id
    ).join(
        Recipe, RecipeIngredient.recipe_id == Recipe.id
    ).filter(
        Recipe.id.in_(recipe_ids)
    ).group_by(
        Ingredient.id, RecipeIngredient.unit
    ).all()
    
    # Convert to list of dictionaries
    return [
        {
            'ingredient_id': row.id,
            'total_quantity': row.total_quantity,
            'unit': row.unit
        }
        for row in result
    ]