import re
from typing import List, Optional
from recipe_scrapers import scrape_me
from app.schemas.recipe import RecipeIngredientCreate
from app.schemas.enums import Unit


def parse_ingredient_string(ingredient_str: str) -> Optional[RecipeIngredientCreate]:
    """
    Parse an ingredient string like "2 cups flour" or "1/2 teaspoon salt"
    into a RecipeIngredientCreate object.
    """
    if not ingredient_str or not ingredient_str.strip():
        return None
    
    # Clean up the ingredient string
    ingredient_str = ingredient_str.strip()
    
    # Common unit mappings
    unit_mappings = {
        # Volume units
        'cup': Unit.CUP,
        'cups': Unit.CUP,
        'c': Unit.CUP,
        'tablespoon': Unit.TABLESPOON,
        'tablespoons': Unit.TABLESPOON,
        'tbsp': Unit.TABLESPOON,
        'tbs': Unit.TABLESPOON,
        'teaspoon': Unit.TEASPOON,
        'teaspoons': Unit.TEASPOON,
        'tsp': Unit.TEASPOON,
        't': Unit.TEASPOON,
        'pint': Unit.PINT,
        'pints': Unit.PINT,
        'pt': Unit.PINT,
        'quart': Unit.QUART,
        'quarts': Unit.QUART,
        'qt': Unit.QUART,
        'gallon': Unit.GALLON,
        'gallons': Unit.GALLON,
        'gal': Unit.GALLON,
        'liter': Unit.LITER,
        'liters': Unit.LITER,
        'l': Unit.LITER,
        'milliliter': Unit.MILLILITER,
        'milliliters': Unit.MILLILITER,
        'ml': Unit.MILLILITER,
        
        # Weight units
        'pound': Unit.POUND,
        'pounds': Unit.POUND,
        'lb': Unit.POUND,
        'lbs': Unit.POUND,
        'ounce': Unit.OUNCE,
        'ounces': Unit.OUNCE,
        'oz': Unit.OUNCE,
        'gram': Unit.GRAM,
        'grams': Unit.GRAM,
        'g': Unit.GRAM,
        'kilogram': Unit.KILOGRAM,
        'kilograms': Unit.KILOGRAM,
        'kg': Unit.KILOGRAM,
        
        # Other units
        'can': Unit.CAN,
        'cans': Unit.CAN,
        'bunch': Unit.BUNCH,
        'bunches': Unit.BUNCH,
        'package': Unit.PACKAGE,
        'packages': Unit.PACKAGE,
        'pkg': Unit.PACKAGE,
        'each': Unit.EACH,
        'piece': Unit.EACH,
        'pieces': Unit.EACH,
    }
    
    # Pattern to match quantity and unit at the beginning
    # Handles fractions like "1/2", "1 1/2", decimals like "2.5", and whole numbers
    quantity_pattern = r'^(\d+(?:\s+\d+/\d+)?|\d+/\d+|\d+\.\d+)\s*([a-zA-Z]+)?\s*(.*)$'
    
    match = re.match(quantity_pattern, ingredient_str, re.IGNORECASE)
    
    if match:
        quantity_str, unit_str, ingredient_name = match.groups()
        
        # Parse quantity (handle fractions and mixed numbers)
        quantity = parse_quantity(quantity_str)
        
        # Parse unit
        unit = Unit.EACH  # default
        if unit_str:
            unit_lower = unit_str.lower()
            unit = unit_mappings.get(unit_lower, Unit.EACH)
        
        # Clean up ingredient name
        ingredient_name = ingredient_name.strip()
        if not ingredient_name:
            # If no ingredient name found, use the whole string as name
            ingredient_name = ingredient_str
        
        return RecipeIngredientCreate(
            name=ingredient_name,
            quantity=quantity,
            unit=unit
        )
    else:
        # No quantity/unit found, treat as a single ingredient
        return RecipeIngredientCreate(
            name=ingredient_str,
            quantity=1.0,
            unit=Unit.EACH
        )


def parse_quantity(quantity_str: str) -> float:
    """Parse quantity string like '1/2', '1 1/2', '2.5', '3' into float."""
    quantity_str = quantity_str.strip()
    
    # Handle mixed numbers like "1 1/2"
    if ' ' in quantity_str and '/' in quantity_str:
        parts = quantity_str.split(' ')
        whole_part = float(parts[0])
        fraction_part = parse_fraction(parts[1])
        return whole_part + fraction_part
    
    # Handle fractions like "1/2"
    if '/' in quantity_str:
        return parse_fraction(quantity_str)
    
    # Handle decimals and whole numbers
    try:
        return float(quantity_str)
    except ValueError:
        return 1.0


def parse_fraction(fraction_str: str) -> float:
    """Parse fraction string like '1/2' into float."""
    try:
        numerator, denominator = fraction_str.split('/')
        return float(numerator) / float(denominator)
    except (ValueError, ZeroDivisionError):
        return 1.0


def parse_ingredients(ingredients_list: List[str]) -> List[RecipeIngredientCreate]:
    """
    Parse a list of ingredient strings into RecipeIngredientCreate objects.
    """
    parsed_ingredients = []
    
    for ingredient_str in ingredients_list:
        parsed = parse_ingredient_string(ingredient_str)
        if parsed:
            parsed_ingredients.append(parsed)
    
    return parsed_ingredients


def scrape_recipe(url: str):
    try:
        scraped = scrape_me(url)
    except Exception as e:
        return "Sorry, we couldn't scrape the recipe from the URL."

    # Parse ingredients into structured format
    parsed_ingredients = parse_ingredients(scraped.ingredients())
    
    return {
        "name": scraped.title(),
        "ingredients": parsed_ingredients,
        "cooking_instructions": scraped.instructions(),
        "total_time": scraped.total_time(),
        "yields": scraped.yields(),
    }

