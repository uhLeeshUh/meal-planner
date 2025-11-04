import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import type { Recipe } from '../types';
import { recipeAPI, groceryListAPI } from '../services/api';

const RecipeViewPage = () => {
  const { id } = useParams<{ id: string }>();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [addingToGroceryList, setAddingToGroceryList] = useState(false);
  const [multiplier, setMultiplier] = useState(1);

  useEffect(() => {
    if (id) {
      fetchRecipe(id);
    }
  }, [id]);

  const fetchRecipe = async (recipeId: string) => {
    try {
      setLoading(true);
      const data = await recipeAPI.getRecipe(recipeId);
      setRecipe(data);
    } catch (err) {
      setError('Failed to fetch recipe');
      console.error('Error fetching recipe:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToGroceryList = async () => {
    if (!recipe) return;

    try {
      setAddingToGroceryList(true);
      // Add the recipe ID multiple times based on multiplier
      // The backend will automatically sum the ingredient quantities
      const recipeIds = Array(multiplier).fill(recipe.id);
      const groceryList = await groceryListAPI.createGroceryList({
        recipe_ids: recipeIds
      });
      
      // Navigate to the grocery list page
      window.location.href = `/grocery-list/${groceryList.id}`;
    } catch (err) {
      console.error('Error creating grocery list:', err);
      alert('Failed to add recipe to grocery list');
    } finally {
      setAddingToGroceryList(false);
    }
  };

  if (loading) return <div className="loading">Loading recipe...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!recipe) return <div className="error">Recipe not found</div>;

  const totalTime = (recipe.prep_time || 0) + recipe.cook_time;

  return (
    <div className="recipe-view-page">
      <div className="recipe-header">
        <nav className="breadcrumb">
          <Link to="/">← Back to Recipes</Link>
        </nav>
        
        <div className="recipe-title-section">
          <h1>{recipe.name}</h1>
          <div className="recipe-actions">
            <div className="multiplier-control">
              <label htmlFor="multiplier">Recipe Multiplier:</label>
              <input
                type="number"
                id="multiplier"
                min="1"
                max="10"
                value={multiplier}
                onChange={(e) => {
                  const value = parseInt(e.target.value, 10);
                  if (!isNaN(value)) {
                    setMultiplier(Math.max(1, Math.min(10, value)));
                  }
                }}
                className="multiplier-input"
              />
              <span className="multiplier-label">{multiplier}x</span>
            </div>
            <button 
              onClick={handleAddToGroceryList}
              disabled={addingToGroceryList}
              className="btn btn-success"
            >
              {addingToGroceryList ? 'Adding...' : 'Add to Grocery List'}
            </button>
          </div>
        </div>

        {recipe.image_url && (
          <div className="recipe-image-container">
            <img 
              src={recipe.image_url} 
              alt={recipe.name}
              className="recipe-main-image"
              onError={(e) => {
                (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          </div>
        )}

        <div className="recipe-meta-info">
          {recipe.prep_time && (
            <div className="meta-item">
              <span className="meta-label">Prep Time:</span>
              <span className="meta-value">{recipe.prep_time} min</span>
            </div>
          )}
          <div className="meta-item">
            <span className="meta-label">Cook Time:</span>
            <span className="meta-value">{recipe.cook_time} min</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Total Time:</span>
            <span className="meta-value">{totalTime} min</span>
          </div>
          {recipe.servings && (
            <div className="meta-item">
              <span className="meta-label">Servings:</span>
              <span className="meta-value">{recipe.servings}</span>
            </div>
          )}
        </div>
      </div>

      <div className="recipe-content">
        <div className="recipe-ingredients">
          <h2>Ingredients {multiplier > 1 && <span className="multiplier-badge">({multiplier}x)</span>}</h2>
          <ul className="ingredients-list">
            {recipe.recipe_ingredients.map((ri) => (
              <li key={ri.id} className="ingredient-item">
                <span className="ingredient-amount">
                  {multiplier > 1 ? (
                    <>
                      <span className="original-quantity">{ri.quantity}</span>
                      <span className="multiplied-quantity"> × {multiplier} = {ri.quantity * multiplier}</span>
                    </>
                  ) : (
                    ri.quantity
                  )} {ri.unit}
                </span>
                <span className="ingredient-name">
                  {ri.ingredient.name}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="recipe-instructions">
          {recipe.prep_instructions && (
            <div className="prep-instructions">
              <h2>Preparation Instructions</h2>
              <div className="instructions-content">
                {recipe.prep_instructions.split('\n').map((line, index) => (
                  <p key={index}>{line}</p>
                ))}
              </div>
            </div>
          )}

          <div className="cooking-instructions">
            <h2>Cooking Instructions</h2>
            <div className="instructions-content">
              {recipe.cooking_instructions.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeViewPage;