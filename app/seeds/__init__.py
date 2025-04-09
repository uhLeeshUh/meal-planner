from app.seeds.recipes import seed_recipes

def run_seeds():
    """Run all seed functions"""
    print("🌱 Starting database seeding...")
    
    seed_recipes()
    
    print("✨ Database seeding completed!") 