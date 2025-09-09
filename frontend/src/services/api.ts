import axios from 'axios';
import type { Recipe, RecipeCreate, GroceryList, CreateGroceryListRequest } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Recipe API endpoints
export const recipeAPI = {
  // Get all recipes with pagination
  getRecipes: async (skip: number = 0, limit: number = 20): Promise<Recipe[]> => {
    const response = await apiClient.get(`/recipes/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get a single recipe by ID
  getRecipe: async (id: string): Promise<Recipe> => {
    const response = await apiClient.get(`/recipes/${id}`);
    return response.data;
  },

  // Create a new recipe
  createRecipe: async (recipe: RecipeCreate): Promise<Recipe> => {
    const response = await apiClient.post('/recipes/', recipe);
    return response.data;
  },
};

// Grocery List API endpoints
export const groceryListAPI = {
  // Create grocery list from recipe IDs
  createGroceryList: async (request: CreateGroceryListRequest): Promise<GroceryList> => {
    const response = await apiClient.post('/grocery-lists/', request);
    return response.data;
  },

  // Get grocery list by ID
  getGroceryList: async (id: string): Promise<GroceryList> => {
    const response = await apiClient.get(`/grocery-lists/${id}`);
    return response.data;
  },
};

// Web scraping utility (to be implemented with backend endpoint)
export const scrapingAPI = {
  // Scrape recipe data from URL
  scrapeRecipe: async (url: string): Promise<Partial<RecipeCreate>> => {
    // TODO: This would need a backend endpoint to handle web scraping
    // For now, return empty data
    console.log('Scraping recipe from:', url);
    return {
      name: '',
      cooking_instructions: '',
      cook_time: 0,
      ingredients: [],
    };
  },
};

export default apiClient;