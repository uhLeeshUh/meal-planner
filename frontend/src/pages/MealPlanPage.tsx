import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { MealPlanRequest } from '../types';
import { mealPlanAPI } from '../services/api';
import RecipeCard from '../components/RecipeCard';

const MealPlanPage = () => {
  const navigate = useNavigate();
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [groceryListId, setGroceryListId] = useState<string | null>(null);
  
  const [formData, setFormData] = useState<MealPlanRequest>({
    num_meals: 7,
    total_time_minutes: undefined,
    preferred_ingredients: [],
    dietary_restrictions: [],
    cuisine_preferences: []
  });
  
  const [ingredientInput, setIngredientInput] = useState('');
  const [dietaryInput, setDietaryInput] = useState('');
  const [cuisineInput, setCuisineInput] = useState('');
  const [generatedRecipes, setGeneratedRecipes] = useState<any[]>([]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? undefined : Number(value)) : value
    }));
  };

  const handleAddIngredient = () => {
    if (ingredientInput.trim()) {
      setFormData(prev => ({
        ...prev,
        preferred_ingredients: [...(prev.preferred_ingredients || []), ingredientInput.trim()]
      }));
      setIngredientInput('');
    }
  };

  const handleRemoveIngredient = (index: number) => {
    setFormData(prev => ({
      ...prev,
      preferred_ingredients: prev.preferred_ingredients?.filter((_, i) => i !== index) || []
    }));
  };

  const handleAddDietary = () => {
    if (dietaryInput.trim()) {
      setFormData(prev => ({
        ...prev,
        dietary_restrictions: [...(prev.dietary_restrictions || []), dietaryInput.trim()]
      }));
      setDietaryInput('');
    }
  };

  const handleRemoveDietary = (index: number) => {
    setFormData(prev => ({
      ...prev,
      dietary_restrictions: prev.dietary_restrictions?.filter((_, i) => i !== index) || []
    }));
  };

  const handleAddCuisine = () => {
    if (cuisineInput.trim()) {
      setFormData(prev => ({
        ...prev,
        cuisine_preferences: [...(prev.cuisine_preferences || []), cuisineInput.trim()]
      }));
      setCuisineInput('');
    }
  };

  const handleRemoveCuisine = (index: number) => {
    setFormData(prev => ({
      ...prev,
      cuisine_preferences: prev.cuisine_preferences?.filter((_, i) => i !== index) || []
    }));
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.num_meals < 1 || formData.num_meals > 20) {
      setError('Number of meals must be between 1 and 20');
      return;
    }

    try {
      setGenerating(true);
      setError(null);
      const response = await mealPlanAPI.generateMealPlan(formData);
      setGeneratedRecipes(response.recipes || []);
      if (response.grocery_list_id) {
        setGroceryListId(response.grocery_list_id);
      }
    } catch (err: any) {
      console.error('Error generating meal plan:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to generate meal plan');
    } finally {
      setGenerating(false);
    }
  };

  const handleViewGroceryList = () => {
    if (groceryListId) {
      navigate(`/grocery-list/${groceryListId}`);
    }
  };

  return (
    <div className="meal-plan-page">
      <h1>Generate Meal Plan</h1>
      
      {error && (
        <div className="error-message" style={{ 
          padding: '1rem', 
          backgroundColor: '#fee', 
          color: '#c33', 
          borderRadius: '4px',
          marginBottom: '1rem'
        }}>
          {error}
        </div>
      )}

      <form onSubmit={handleGenerate} className="meal-plan-form">
        <div className="form-group">
          <label htmlFor="num_meals">Number of Meals *</label>
          <input
            type="number"
            id="num_meals"
            name="num_meals"
            value={formData.num_meals}
            onChange={handleInputChange}
            required
            min="1"
            max="20"
            className="form-control"
          />
        </div>

        <div className="form-group">
          <label htmlFor="total_time_minutes">Total Time Available (minutes)</label>
          <input
            type="number"
            id="total_time_minutes"
            name="total_time_minutes"
            value={formData.total_time_minutes || ''}
            onChange={handleInputChange}
            min="0"
            className="form-control"
            placeholder="e.g., 300 for 5 hours total"
          />
          <small className="help-text">
            Total time you have to prepare all meals. The AI will divide this across recipes.
          </small>
        </div>

        <div className="form-group">
          <label>Preferred Ingredients</label>
          <div className="tag-input-group">
            <input
              type="text"
              value={ingredientInput}
              onChange={(e) => setIngredientInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddIngredient();
                }
              }}
              placeholder="e.g., chicken, tomatoes, pasta"
              className="form-control"
            />
            <button
              type="button"
              onClick={handleAddIngredient}
              className="btn btn-secondary"
            >
              Add
            </button>
          </div>
          {formData.preferred_ingredients && formData.preferred_ingredients.length > 0 && (
            <div className="tag-list">
              {formData.preferred_ingredients.map((ing, index) => (
                <span key={index} className="tag">
                  {ing}
                  <button
                    type="button"
                    onClick={() => handleRemoveIngredient(index)}
                    className="tag-remove"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="form-group">
          <label>Dietary Restrictions</label>
          <div className="tag-input-group">
            <input
              type="text"
              value={dietaryInput}
              onChange={(e) => setDietaryInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddDietary();
                }
              }}
              placeholder="e.g., vegetarian, gluten-free, dairy-free"
              className="form-control"
            />
            <button
              type="button"
              onClick={handleAddDietary}
              className="btn btn-secondary"
            >
              Add
            </button>
          </div>
          {formData.dietary_restrictions && formData.dietary_restrictions.length > 0 && (
            <div className="tag-list">
              {formData.dietary_restrictions.map((diet, index) => (
                <span key={index} className="tag">
                  {diet}
                  <button
                    type="button"
                    onClick={() => handleRemoveDietary(index)}
                    className="tag-remove"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="form-group">
          <label>Cuisine Preferences</label>
          <div className="tag-input-group">
            <input
              type="text"
              value={cuisineInput}
              onChange={(e) => setCuisineInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddCuisine();
                }
              }}
              placeholder="e.g., Italian, Mexican, Asian"
              className="form-control"
            />
            <button
              type="button"
              onClick={handleAddCuisine}
              className="btn btn-secondary"
            >
              Add
            </button>
          </div>
          {formData.cuisine_preferences && formData.cuisine_preferences.length > 0 && (
            <div className="tag-list">
              {formData.cuisine_preferences.map((cuisine, index) => (
                <span key={index} className="tag">
                  {cuisine}
                  <button
                    type="button"
                    onClick={() => handleRemoveCuisine(index)}
                    className="tag-remove"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="form-actions">
          <button
            type="submit"
            disabled={generating}
            className="btn btn-primary"
          >
            {generating ? 'Generating Meal Plan...' : 'Generate Meal Plan'}
          </button>
        </div>
      </form>

      {generatedRecipes.length > 0 && (
        <div className="generated-meal-plan" style={{ marginTop: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>Generated Recipes</h2>
            {groceryListId && (
              <button
                onClick={handleViewGroceryList}
                className="btn btn-success"
              >
                View Grocery List
              </button>
            )}
          </div>
          <div className="recipes-grid">
            {generatedRecipes.map((recipe) => (
              <RecipeCard
                key={recipe.id}
                recipe={recipe}
                isSelected={false}
                onSelect={() => {}}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MealPlanPage;




