import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { RecipeCreate, RecipeIngredientCreate } from '../types';
import { recipeAPI, scrapingAPI } from '../services/api';

const CreateRecipePage = () => {
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState<RecipeCreate>({
    name: '',
    prep_instructions: '',
    cooking_instructions: '',
    prep_time: undefined,
    cook_time: 0,
    servings: undefined,
    image_url: '',
    ingredients: []
  });
  
  const [urlToScrape, setUrlToScrape] = useState('');
  const [scraping, setScraping] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [newIngredient, setNewIngredient] = useState<RecipeIngredientCreate>({
    name: '',
    quantity: 0,
    unit: 'cups'
  });

  const units = [
    'cups', 'tbsp', 'tsp', 'oz', 'lbs', 'g', 'kg', 'ml', 'l', 
    'pieces', 'cloves', 'slices', 'whole', 'pinch', 'dash'
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setRecipe(prev => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? undefined : Number(value)) : value
    }));
  };

  const handleScrapeUrl = async () => {
    if (!urlToScrape.trim()) {
      alert('Please enter a valid URL');
      return;
    }

    try {
      setScraping(true);
      const scrapedData = await scrapingAPI.scrapeRecipe(urlToScrape);
      
      setRecipe(prev => ({
        ...prev,
        ...scrapedData,
        // Only update fields that have data from scraping
        name: scrapedData.name || prev.name,
        cooking_instructions: scrapedData.cooking_instructions || prev.cooking_instructions,
        cook_time: scrapedData.cook_time || prev.cook_time,
        prep_time: scrapedData.prep_time || prev.prep_time,
        servings: scrapedData.servings || prev.servings,
        image_url: scrapedData.image_url || prev.image_url,
        ingredients: scrapedData.ingredients || prev.ingredients
      }));
      
      alert('Recipe data scraped successfully! Please review and edit as needed.');
    } catch (err) {
      console.error('Error scraping recipe:', err);
      alert('Failed to scrape recipe. Please fill out the form manually.');
    } finally {
      setScraping(false);
    }
  };

  const handleAddIngredient = () => {
    if (!newIngredient.name.trim() || newIngredient.quantity <= 0) {
      alert('Please enter ingredient name and quantity');
      return;
    }

    setRecipe(prev => ({
      ...prev,
      ingredients: [...prev.ingredients, { ...newIngredient }]
    }));

    setNewIngredient({
      name: '',
      quantity: 0,
      unit: 'cups'
    });
  };

  const handleRemoveIngredient = (index: number) => {
    setRecipe(prev => ({
      ...prev,
      ingredients: prev.ingredients.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!recipe.name.trim() || !recipe.cooking_instructions.trim() || recipe.ingredients.length === 0) {
      alert('Please fill out all required fields and add at least one ingredient');
      return;
    }

    try {
      setSubmitting(true);
      const newRecipe = await recipeAPI.createRecipe(recipe);
      navigate(`/recipe/${newRecipe.id}`);
    } catch (err) {
      console.error('Error creating recipe:', err);
      alert('Failed to create recipe. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="create-recipe-page">
      <h1>Create New Recipe</h1>

      <div className="url-scraper-section">
        <h2>Import from URL (Optional)</h2>
        <div className="url-input-group">
          <input
            type="url"
            placeholder="Paste recipe URL here..."
            value={urlToScrape}
            onChange={(e) => setUrlToScrape(e.target.value)}
            className="url-input"
          />
          <button
            type="button"
            onClick={handleScrapeUrl}
            disabled={scraping || !urlToScrape.trim()}
            className="btn btn-secondary"
          >
            {scraping ? 'Scraping...' : 'Import Recipe'}
          </button>
        </div>
        <p className="help-text">
          Paste a URL from a recipe website to auto-fill the form below.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="recipe-form">
        <div className="form-group">
          <label htmlFor="name">Recipe Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={recipe.name}
            onChange={handleInputChange}
            required
            className="form-control"
          />
        </div>

        <div className="form-group">
          <label htmlFor="image_url">Image URL</label>
          <input
            type="url"
            id="image_url"
            name="image_url"
            value={recipe.image_url || ''}
            onChange={handleInputChange}
            className="form-control"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="prep_time">Prep Time (minutes)</label>
            <input
              type="number"
              id="prep_time"
              name="prep_time"
              value={recipe.prep_time || ''}
              onChange={handleInputChange}
              min="0"
              className="form-control"
            />
          </div>
          <div className="form-group">
            <label htmlFor="cook_time">Cook Time (minutes) *</label>
            <input
              type="number"
              id="cook_time"
              name="cook_time"
              value={recipe.cook_time}
              onChange={handleInputChange}
              required
              min="0"
              className="form-control"
            />
          </div>
          <div className="form-group">
            <label htmlFor="servings">Servings</label>
            <input
              type="number"
              id="servings"
              name="servings"
              value={recipe.servings || ''}
              onChange={handleInputChange}
              min="1"
              className="form-control"
            />
          </div>
        </div>

        <div className="ingredients-section">
          <h3>Ingredients</h3>
          
          <div className="add-ingredient">
            <div className="ingredient-input-group">
              <input
                type="number"
                placeholder="Quantity"
                value={newIngredient.quantity || ''}
                onChange={(e) => setNewIngredient(prev => ({
                  ...prev,
                  quantity: Number(e.target.value)
                }))}
                min="0"
                step="0.25"
                className="quantity-input"
              />
              <select
                value={newIngredient.unit}
                onChange={(e) => setNewIngredient(prev => ({
                  ...prev,
                  unit: e.target.value
                }))}
                className="unit-select"
              >
                {units.map(unit => (
                  <option key={unit} value={unit}>{unit}</option>
                ))}
              </select>
              <input
                type="text"
                placeholder="Ingredient name"
                value={newIngredient.name}
                onChange={(e) => setNewIngredient(prev => ({
                  ...prev,
                  name: e.target.value
                }))}
                className="ingredient-name-input"
              />
              <button
                type="button"
                onClick={handleAddIngredient}
                className="btn btn-success btn-sm"
              >
                Add
              </button>
            </div>
          </div>

          <ul className="ingredients-list">
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index} className="ingredient-item">
                <span>
                  {ingredient.quantity} {ingredient.unit} {ingredient.name}
                </span>
                <button
                  type="button"
                  onClick={() => handleRemoveIngredient(index)}
                  className="btn btn-danger btn-sm"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="form-group">
          <label htmlFor="prep_instructions">Preparation Instructions</label>
          <textarea
            id="prep_instructions"
            name="prep_instructions"
            value={recipe.prep_instructions || ''}
            onChange={handleInputChange}
            rows={4}
            className="form-control"
            placeholder="Optional preparation steps..."
          />
        </div>

        <div className="form-group">
          <label htmlFor="cooking_instructions">Cooking Instructions *</label>
          <textarea
            id="cooking_instructions"
            name="cooking_instructions"
            value={recipe.cooking_instructions}
            onChange={handleInputChange}
            required
            rows={6}
            className="form-control"
            placeholder="Step-by-step cooking instructions..."
          />
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="btn btn-secondary"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="btn btn-primary"
          >
            {submitting ? 'Creating...' : 'Create Recipe'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateRecipePage;