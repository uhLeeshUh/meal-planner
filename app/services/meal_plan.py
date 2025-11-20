from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.meal_plan import MealPlanRequest, MealPlanResponse
from app.schemas.recipe import Recipe, RecipeCreate
from app.core.dependencies import get_llm_service
from app.repositories.recipes import create_recipe, search_recipes_by_ingredients
from app.services.grocery_list import build_grocery_list
import random

def create_meal_plan_with_grocery_list(
    db: Session,
    request: MealPlanRequest,
    create_grocery_list: bool = True,
    prefer_existing_recipes: bool = True
) -> MealPlanResponse:
    """
    Generate a meal plan by first trying to use existing recipes from the database,
    then using LLM to generate any remaining recipes needed.
    """
    selected_recipe_ids = []
    selected_recipes = []
    
    # Calculate max time per recipe if total time is provided
    max_time_per_recipe = None
    if request.total_time_minutes:
        max_time_per_recipe = request.total_time_minutes // request.num_meals
    
    # Try to find existing recipes from database if preferred
    if prefer_existing_recipes:
        if request.preferred_ingredients:
            # Search by preferred ingredients
            existing_recipes = search_recipes_by_ingredients(
                db=db,
                ingredient_names=request.preferred_ingredients,
                max_time_minutes=max_time_per_recipe,
                limit=request.num_meals * 2  # Get more than needed for variety
            )
        else:
            # If no preferred ingredients, get all recipes (up to limit)
            from app.repositories.recipes import get_recipes
            existing_recipes = get_recipes(
                db=db,
                page_number=0,
                page_size=request.num_meals * 2
            )
            # Filter by time if specified
            if max_time_per_recipe is not None:
                existing_recipes = [
                    r for r in existing_recipes
                    if (r.prep_time or 0) + r.cook_time <= max_time_per_recipe
                ]
        
        # Randomly select up to the requested number of meals
        if existing_recipes:
            num_to_select = min(len(existing_recipes), request.num_meals)
            if num_to_select > 0:
                if num_to_select == len(existing_recipes):
                    selected_existing = existing_recipes
                else:
                    selected_existing = random.sample(existing_recipes, num_to_select)
                
                for recipe_model in selected_existing:
                    selected_recipe_ids.append(recipe_model.id)
                    selected_recipes.append(Recipe.model_validate(recipe_model))
    
    # Calculate how many more recipes we need
    num_remaining = request.num_meals - len(selected_recipes)
    
    # If we need more recipes, generate them using LLM
    if num_remaining > 0:
        # Get the LLM service (singleton, managed internally by the service layer)
        llm_service = get_llm_service()
        
        # Create a modified request for the LLM with remaining count
        llm_request = MealPlanRequest(
            num_meals=num_remaining,
            total_time_minutes=request.total_time_minutes,
            preferred_ingredients=request.preferred_ingredients,
            dietary_restrictions=request.dietary_restrictions,
            cuisine_preferences=request.cuisine_preferences
        )
        
        # Generate meal plan using LLM (returns RecipeCreate objects)
        llm_response = llm_service.generate_meal_plan(llm_request)
        
        # Create the generated recipes in the database
        for recipe_create in llm_response.recipes:
            created_recipe_model = create_recipe(db, recipe_create)
            selected_recipe_ids.append(created_recipe_model.id)
            # Convert SQLAlchemy model to Pydantic schema
            selected_recipes.append(Recipe.model_validate(created_recipe_model))
    
    # Create grocery list if requested
    grocery_list_id = None
    if create_grocery_list and selected_recipe_ids:
        grocery_list = build_grocery_list(db, selected_recipe_ids)
        grocery_list_id = str(grocery_list.id)
    
    # Return response with selected recipes (mix of existing and generated) and grocery list ID
    return MealPlanResponse(
        recipes=selected_recipes,
        grocery_list_id=grocery_list_id
    )

