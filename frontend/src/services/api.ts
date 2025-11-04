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

// Web scraping utility
export const scrapingAPI = {
  // Scrape recipe data from URL
  scrapeRecipe: async (url: string): Promise<Partial<RecipeCreate>> => {
    const response = await apiClient.post('/recipes/scrape', { url });
    const scrapedData = response.data;

    // Handle error response (backend returns string on error)
    if (typeof scrapedData === 'string') {
      throw new Error(scrapedData);
    }

    // Parse yields (could be "4 servings", "4", etc.)
    let servings: number | undefined;
    if (scrapedData.yields) {
      const yieldsMatch = scrapedData.yields.toString().match(/\d+/);
      if (yieldsMatch) {
        servings = parseInt(yieldsMatch[0], 10);
      }
    }

    // Map backend response to frontend RecipeCreate format
    // total_time might be combined prep+cook time, so we'll assign it to cook_time
    // If you need to split it, you'd need backend changes
    const cookTime = scrapedData.total_time ? parseInt(scrapedData.total_time.toString(), 10) : 0;

    return {
      name: scrapedData.name || '',
      cooking_instructions: scrapedData.cooking_instructions || '',
      cook_time: cookTime,
      servings: servings,
      ingredients: scrapedData.ingredients || [],
    };
  },
};

export default apiClient;