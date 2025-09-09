import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import type { Recipe, SelectedRecipes } from '../types';
import { recipeAPI, groceryListAPI } from '../services/api';
import RecipeCard from '../components/RecipeCard';
import Pagination from '../components/Pagination';

const HomePage = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedRecipes, setSelectedRecipes] = useState<SelectedRecipes>({});
  const [creatingGroceryList, setCreatingGroceryList] = useState(false);
  
  const recipesPerPage = 12;

  useEffect(() => {
    fetchRecipes();
  }, [currentPage]);

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      const skip = (currentPage - 1) * recipesPerPage;
      const data = await recipeAPI.getRecipes(skip, recipesPerPage);
      setRecipes(data);
    } catch (err) {
      setError('Failed to fetch recipes');
      console.error('Error fetching recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectRecipe = (recipeId: string, isSelected: boolean) => {
    setSelectedRecipes(prev => ({
      ...prev,
      [recipeId]: isSelected
    }));
  };

  const handleCreateGroceryList = async () => {
    const selectedRecipeIds = Object.entries(selectedRecipes)
      .filter(([_, isSelected]) => isSelected)
      .map(([recipeId]) => recipeId);

    if (selectedRecipeIds.length === 0) {
      alert('Please select at least one recipe to create a grocery list');
      return;
    }

    try {
      setCreatingGroceryList(true);
      const groceryList = await groceryListAPI.createGroceryList({
        recipe_ids: selectedRecipeIds
      });
      
      // Navigate to the grocery list page
      window.location.href = `/grocery-list/${groceryList.id}`;
    } catch (err) {
      console.error('Error creating grocery list:', err);
      alert('Failed to create grocery list');
    } finally {
      setCreatingGroceryList(false);
    }
  };

  const selectedCount = Object.values(selectedRecipes).filter(Boolean).length;

  if (loading) return <div className="loading">Loading recipes...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="home-page">
      <div className="page-header">
        <h1>Recipe Collection</h1>
        <Link to="/create-recipe" className="btn btn-primary">
          Add New Recipe
        </Link>
      </div>

      {selectedCount > 0 && (
        <div className="selected-recipes-bar">
          <span>{selectedCount} recipe{selectedCount > 1 ? 's' : ''} selected</span>
          <button 
            onClick={handleCreateGroceryList}
            disabled={creatingGroceryList}
            className="btn btn-success"
          >
            {creatingGroceryList ? 'Creating...' : 'Create Grocery List'}
          </button>
          <button 
            onClick={() => setSelectedRecipes({})}
            className="btn btn-secondary"
          >
            Clear Selection
          </button>
        </div>
      )}

      <div className="recipes-grid">
        {recipes.map(recipe => (
          <RecipeCard
            key={recipe.id}
            recipe={recipe}
            isSelected={selectedRecipes[recipe.id] || false}
            onSelect={handleSelectRecipe}
          />
        ))}
      </div>

      {recipes.length === 0 && !loading && (
        <div className="empty-state">
          <h2>No recipes yet</h2>
          <p>Get started by creating your first recipe!</p>
          <Link to="/create-recipe" className="btn btn-primary">
            Create Recipe
          </Link>
        </div>
      )}

      <Pagination
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        hasMore={recipes.length === recipesPerPage}
      />
    </div>
  );
};

export default HomePage;