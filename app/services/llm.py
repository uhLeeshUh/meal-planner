import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas.meal_plan import MealPlanRequest
from app.schemas.recipe import RecipeCreate, RecipeIngredientCreate
from app.schemas.enums import Unit

load_dotenv()

class LLMService:
    """Service for interacting with LLM providers to generate meal plans"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    def generate_meal_plan(self, request: MealPlanRequest):
        """
        Generate a meal plan based on user constraints using an LLM.
        Returns a list of recipes and can optionally create a grocery list.
        """
        prompt = self._build_meal_plan_prompt(request)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful meal planning assistant. You generate detailed, realistic recipes in JSON format. Always return valid JSON that matches the exact schema requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from LLM")
            
            # Parse the JSON response
            meal_plan_data = json.loads(content)
            
            # Convert to RecipeCreate objects
            recipes = []
            if "recipes" in meal_plan_data:
                for recipe_data in meal_plan_data["recipes"]:
                    # Parse ingredients
                    ingredients = []
                    if "ingredients" in recipe_data:
                        for ing in recipe_data["ingredients"]:
                            # Map unit string to Unit enum
                            unit_str = ing.get("unit", "each").lower()
                            unit = self._parse_unit(unit_str)
                            
                            ingredients.append(RecipeIngredientCreate(
                                name=ing.get("name", ""),
                                quantity=float(ing.get("quantity", 1)),
                                unit=unit
                            ))
                    
                    recipe = RecipeCreate(
                        name=recipe_data.get("name", "Unnamed Recipe"),
                        prep_instructions=recipe_data.get("prep_instructions", ""),
                        cooking_instructions=recipe_data.get("cooking_instructions", ""),
                        prep_time=recipe_data.get("prep_time"),
                        cook_time=recipe_data.get("cook_time"),
                        servings=recipe_data.get("servings"),
                        image_url=recipe_data.get("image_url"),
                        ingredients=ingredients
                    )
                    recipes.append(recipe)
            
            # Return a simple object with recipes (RecipeCreate objects)
            # The service layer will convert these to Recipe objects with IDs
            from types import SimpleNamespace
            return SimpleNamespace(recipes=recipes)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            raise ValueError(f"Error generating meal plan: {str(e)}")
    
    def _build_meal_plan_prompt(self, request: MealPlanRequest) -> str:
        """Build the prompt for meal plan generation"""
        constraints = []
        
        constraints.append(f"Generate exactly {request.num_meals} recipes for a weekly meal plan.")
        
        if request.total_time_minutes:
            avg_time = request.total_time_minutes // request.num_meals
            constraints.append(f"Each recipe should take approximately {avg_time} minutes or less to prepare and cook (total prep_time + cook_time).")
        
        if request.preferred_ingredients:
            constraints.append(f"Prioritize using these ingredients: {', '.join(request.preferred_ingredients)}.")
        
        if request.dietary_restrictions:
            constraints.append(f"Follow these dietary restrictions: {', '.join(request.dietary_restrictions)}.")
        
        if request.cuisine_preferences:
            constraints.append(f"Focus on these cuisines: {', '.join(request.cuisine_preferences)}.")
        
        prompt = f"""Generate a meal plan with the following constraints:
{"\n".join(f"- {c}" for c in constraints)}

Return a JSON object with this exact structure:
{{
  "recipes": [
    {{
      "name": "Recipe Name",
      "prep_instructions": "Optional preparation steps",
      "cooking_instructions": "Detailed cooking instructions",
      "prep_time": 15,
      "cook_time": 30,
      "servings": 4,
      "image_url": null,
      "ingredients": [
        {{
          "name": "Ingredient Name",
          "quantity": 2.0,
          "unit": "cup"
        }}
      ]
    }}
  ]
}}

Important:
- Include detailed, realistic cooking instructions
- Use standard units: "each", "cup", "tablespoon", "teaspoon", "gram", "kilogram", "ounce", "pound", "milliliter", "liter", "can", "bunch", "package"
- Ensure prep_time + cook_time matches the time constraint if provided
- Make recipes diverse and interesting
- Include all necessary ingredients with realistic quantities"""
        
        return prompt
    
    def _parse_unit(self, unit_str: str) -> Unit:
        """Parse a unit string to Unit enum, with fallback to EACH"""
        unit_mapping = {
            "each": Unit.EACH,
            "cup": Unit.CUP,
            "cups": Unit.CUP,
            "tablespoon": Unit.TABLESPOON,
            "tablespoons": Unit.TABLESPOON,
            "tbsp": Unit.TABLESPOON,
            "teaspoon": Unit.TEASPOON,
            "teaspoons": Unit.TEASPOON,
            "tsp": Unit.TEASPOON,
            "gram": Unit.GRAM,
            "grams": Unit.GRAM,
            "g": Unit.GRAM,
            "kilogram": Unit.KILOGRAM,
            "kilograms": Unit.KILOGRAM,
            "kg": Unit.KILOGRAM,
            "ounce": Unit.OUNCE,
            "ounces": Unit.OUNCE,
            "oz": Unit.OUNCE,
            "pound": Unit.POUND,
            "pounds": Unit.POUND,
            "lb": Unit.POUND,
            "lbs": Unit.POUND,
            "milliliter": Unit.MILLILITER,
            "milliliters": Unit.MILLILITER,
            "ml": Unit.MILLILITER,
            "liter": Unit.LITER,
            "liters": Unit.LITER,
            "l": Unit.LITER,
            "gallon": Unit.GALLON,
            "gallons": Unit.GALLON,
            "pint": Unit.PINT,
            "pints": Unit.PINT,
            "quart": Unit.QUART,
            "quarts": Unit.QUART,
            "can": Unit.CAN,
            "cans": Unit.CAN,
            "bunch": Unit.BUNCH,
            "bunches": Unit.BUNCH,
            "package": Unit.PACKAGE,
            "packages": Unit.PACKAGE,
            "pkg": Unit.PACKAGE,
        }
        
        normalized = unit_str.lower().strip()
        return unit_mapping.get(normalized, Unit.EACH)

