from app.core.database import SessionLocal
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeIngredientCreate
from app.schemas.enums import Unit
from app.repositories.recipes import create_recipe

def seed_recipes():
    db = SessionLocal()
    try:
        # Sample recipes with ingredients included directly in the schema
        recipe_schemas = [
            RecipeCreate(
                name="Spaghetti Carbonara",
                prep_instructions="1. Bring a large pot of salted water to boil\n2. Cook spaghetti according to package instructions",
                cooking_instructions="1. Cook pancetta until crispy\n2. Mix eggs and cheese\n3. Combine hot pasta with egg mixture and pancetta\n4. Add black pepper to taste",
                prep_time=15,
                cook_time=20,
                servings=4,
                image_url="https://example.com/carbonara.jpg",
                ingredients=[
                    RecipeIngredientCreate(name="Spaghetti", quantity=400, unit=Unit.GRAM),
                    RecipeIngredientCreate(name="Pancetta", quantity=150, unit=Unit.GRAM),
                    RecipeIngredientCreate(name="Eggs", quantity=4, unit=Unit.EACH),
                    RecipeIngredientCreate(name="Parmesan Cheese", quantity=100, unit=Unit.GRAM),
                    RecipeIngredientCreate(name="Onion", quantity=1, unit=Unit.EACH),
                    RecipeIngredientCreate(name="Salt", quantity=1, unit=Unit.TEASPOON),
                    RecipeIngredientCreate(name="Black Pepper", quantity=0.5, unit=Unit.TEASPOON),
                ]
            ),
            RecipeCreate(
                name="Classic Burger",
                prep_instructions="1. Form patties\n2. Season with salt and pepper",
                cooking_instructions="1. Grill patties for 4-5 minutes per side\n2. Add cheese if desired\n3. Toast buns\n4. Assemble with lettuce, tomato, and onion",
                prep_time=10,
                cook_time=15,
                servings=4,
                image_url="https://example.com/burger.jpg",
                ingredients=[
                    RecipeIngredientCreate(name="Ground Beef", quantity=500, unit=Unit.GRAM),
                    RecipeIngredientCreate(name="Burger Buns", quantity=4, unit=Unit.EACH),
                    RecipeIngredientCreate(name="Cheddar Cheese", quantity=4, unit=Unit.EACH),
                    RecipeIngredientCreate(name="Lettuce", quantity=1, unit=Unit.BUNCH),
                    RecipeIngredientCreate(name="Tomato", quantity=2, unit=Unit.EACH),
                    RecipeIngredientCreate(name="Onion", quantity=1, unit=Unit.EACH),  # Shared with Carbonara
                    RecipeIngredientCreate(name="Salt", quantity=1, unit=Unit.TEASPOON),   # Shared with all recipes
                    RecipeIngredientCreate(name="Black Pepper", quantity=0.5, unit=Unit.TEASPOON),  # Shared with Carbonara
                ]
            ),
            RecipeCreate(
                name="Greek Salad",
                prep_instructions="1. Wash and chop vegetables\n2. Cube feta cheese",
                cooking_instructions="1. Combine all ingredients in a large bowl\n2. Toss with olive oil and lemon juice\n3. Season with salt and oregano",
                prep_time=15,
                cook_time=0,
                servings=4,
                image_url="https://example.com/greek-salad.jpg",
                ingredients=[
                    RecipeIngredientCreate(name="Cucumber", quantity=2, unit=Unit.EACH),
                    RecipeIngredientCreate(name="Feta Cheese", quantity=200, unit=Unit.GRAM),
                    RecipeIngredientCreate(name="Kalamata Olives", quantity=100, unit=Unit.GRAM),
                    RecipeIngredientCreate(name="Olive Oil", quantity=3, unit=Unit.TABLESPOON),
                    RecipeIngredientCreate(name="Lemon Juice", quantity=2, unit=Unit.TABLESPOON),
                    RecipeIngredientCreate(name="Oregano", quantity=1, unit=Unit.TEASPOON),
                    RecipeIngredientCreate(name="Salt", quantity=0.5, unit=Unit.TEASPOON),  # Shared with all recipes
                ]
            )
        ]

        # Create recipes using the repository function
        for schema in recipe_schemas:
            create_recipe(db, schema)
        
        print("✅ Recipes, ingredients, and recipe_ingredients seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding recipes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_recipes() 