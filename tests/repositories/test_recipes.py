from unittest.mock import MagicMock
from app.repositories.recipes import create_recipe
from app.schemas.recipe import RecipeCreate

def test_create_recipe():
    # Mock the database session
    mock_session = MagicMock()

    # create existing ingredient for recipe
    from app.models.ingredient import Ingredient

    existing_ingredient = Ingredient(name="cheese")
    mock_session.add(existing_ingredient)
    mock_session.commit()
    mock_session.refresh(existing_ingredient)

    # Define test data
    recipe_data = {
        "name": "Test Recipe",
        "cooking_instructions": "Cook thoroughly.",
        "cook_time": 30,
        "ingredients": [
            existing_ingredient.model_to_dict(),
            {"name": "New ingredient"}
        ]
    }

    # Call the create function
    created_recipe = create_recipe(mock_session, RecipeCreate(**recipe_data))

    # Assertions
    assert created_recipe.name == recipe_data["name"]
    assert created_recipe.cooking_instructions == recipe_data["cooking_instructions"]
    assert created_recipe.cook_time == recipe_data["cook_time"]
    assert len(created_recipe.ingredients) == len(recipe_data["ingredients"])