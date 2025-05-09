from enum import Enum

# This enum inherits from both Enum and str so that it can be used in SA and pydantic models
# Units inspired from Instacart docs https://docs.instacart.com/developer_platform_api/api/units_of_measurement/
class Unit(str, Enum):
    EACH = "each" # Default for countable items, e.g. tomatoes or onions
    CUP = "cup"
    TABLESPOON = "tablespoon"
    TEASPOON = "teaspoon"
    GRAM = "gram"
    KILOGRAM = "kilogram"
    OUNCE = "ounce"
    POUND = "pound"
    GALLON = "gallon"
    MILLILITER = "milliliter"
    LITER = "liter"
    PINT = "pint"
    QUART = "quart"
    CAN = "can"
    BUNCH = "bunch"
    PACKAGE = "package"