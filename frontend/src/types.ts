// API Types matching the backend schemas

export interface Ingredient {
  id: string;
  name: string;
}

export interface RecipeIngredient {
  id: string;
  recipe_id: string;
  ingredient_id: string;
  quantity: number;
  unit: string;
  ingredient: Ingredient;
}

export interface Recipe {
  id: string;
  name: string;
  prep_instructions?: string;
  cooking_instructions: string;
  prep_time?: number;
  cook_time: number;
  servings?: number;
  image_url?: string;
  recipe_ingredients: RecipeIngredient[];
}

export interface RecipeCreate {
  name: string;
  prep_instructions?: string;
  cooking_instructions: string;
  prep_time?: number;
  cook_time: number;
  servings?: number;
  image_url?: string;
  ingredients: RecipeIngredientCreate[];
}

export interface RecipeIngredientCreate {
  name: string;
  quantity: number;
  unit: string;
}

export interface GroceryListItem {
  id: string;
  grocery_list_id: string;
  ingredient_id: string;
  quantity: number;
  unit: string;
  ingredient: Ingredient;
}

export interface GroceryList {
  id: string;
  items?: GroceryListItem[];
}

// Request types
export interface CreateGroceryListRequest {
  recipe_ids: string[];
}

// UI State types
export interface PaginationState {
  page: number;
  limit: number;
  total: number;
}

export interface SelectedRecipes {
  [recipeId: string]: boolean;
}