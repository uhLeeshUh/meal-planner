from unittest.mock import MagicMock
from app.repositories.recipes import create_recipe
from app.schemas.recipe import RecipeCreate
from app.schemas.ingredient import Ingredient, IngredientCreate
import uuid

def test_create_recipe():
    # Mock the database session
    mock_session = MagicMock()

    existing_ingredient = Ingredient(id=str(uuid.uuid4()), name="cheddar cheese")
    new_ingredient = IngredientCreate(name="celery")

    # Define test data
    recipe_data = {
        "name": "Test Recipe",
        "cooking_instructions": "Cook thoroughly.",
        "cook_time": 30,
        "ingredients": [
            existing_ingredient,
            new_ingredient
        ]
    }

    # Call the create function
    created_recipe = create_recipe(mock_session, RecipeCreate(**recipe_data))

    # Assertions
    assert created_recipe.name == recipe_data["name"]
    assert created_recipe.cooking_instructions == recipe_data["cooking_instructions"]
    assert created_recipe.cook_time == recipe_data["cook_time"]

    assert len(created_recipe.ingredients) == len(recipe_data["ingredients"])
    # only new ingredient and new recipe were added to db
    assert mock_session.add.call_count == 2