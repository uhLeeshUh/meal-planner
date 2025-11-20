import chromadb
from dotenv import load_dotenv

from app.core.database import SessionLocal
from app.core.dependencies import get_llm_service
from app.shared.constants import RECIPE_COLLECTION
from app.repositories.recipes import get_recipes

load_dotenv()

def create_recipe_embeddings():
    # connect to OpenAI to generate embeddings for recipes
    llm_service = get_llm_service()

    # connect to local vector db
    vector_db = chromadb.PersistentClient(path="./chromadb")
    collection = vector_db.get_or_create_collection(RECIPE_COLLECTION)

    db = SessionLocal()

    try:
        # do an initial query of all recipes in db
        recipes = get_recipes(db=db, page_number=0, page_size=1000)

        for recipe in recipes:
            text_representation = f"{recipe.name}\n{recipe.cooking_instructions}\n{recipe.recipe_ingredients}"

            embedding = llm_service.generate_embedding(text=text_representation)

            collection.add(ids=[str(recipe.id)], embeddings=[embedding], documents=[text_representation])

            print(f"Successfully added recipe {recipe.id}:{recipe.name}")

    except Exception as e:
        print(f"❌ Error embedding recipes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_recipe_embeddings() 