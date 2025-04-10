from app.core.database import SessionLocal
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate

def seed_recipes():
    db = SessionLocal()
    try:
        # Sample recipes using Pydantic schemas for validation
        recipe_schemas = [
            RecipeCreate(
                name="Spaghetti Carbonara",
                prep_instructions="1. Bring a large pot of salted water to boil\n2. Cook spaghetti according to package instructions",
                cooking_instructions="1. Cook pancetta until crispy\n2. Mix eggs and cheese\n3. Combine hot pasta with egg mixture and pancetta\n4. Add black pepper to taste",
                prep_time=15,
                cook_time=20,
                servings=4,
                image_url="https://example.com/carbonara.jpg"
            ),
            RecipeCreate(
                name="Classic Burger",
                prep_instructions="1. Form patties\n2. Season with salt and pepper",
                cooking_instructions="1. Grill patties for 4-5 minutes per side\n2. Add cheese if desired\n3. Toast buns\n4. Assemble with lettuce, tomato, and onion",
                prep_time=10,
                cook_time=15,
                servings=4,
                image_url="https://example.com/burger.jpg"
            ),
            RecipeCreate(
                name="Greek Salad",
                prep_instructions="1. Wash and chop vegetables\n2. Cube feta cheese",
                cooking_instructions="1. Combine all ingredients in a large bowl\n2. Toss with olive oil and lemon juice\n3. Season with salt and oregano",
                prep_time=15,
                cook_time=0,
                servings=4,
                image_url="https://example.com/greek-salad.jpg"
            )
        ]

        # Convert schemas to models and add to database
        for schema in recipe_schemas:
            recipe = Recipe.from_schema(schema)
            db.add(recipe)
        
        db.commit()
        print("✅ Recipes seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding recipes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_recipes() 