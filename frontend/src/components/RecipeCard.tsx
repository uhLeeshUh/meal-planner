import { Link } from 'react-router-dom';
import type { Recipe } from '../types';

interface RecipeCardProps {
  recipe: Recipe;
  isSelected: boolean;
  onSelect: (recipeId: string, isSelected: boolean) => void;
}

const RecipeCard = ({ recipe, isSelected, onSelect }: RecipeCardProps) => {
  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onSelect(recipe.id, e.target.checked);
  };

  const totalTime = (recipe.prep_time || 0) + recipe.cook_time;

  return (
    <div className={`recipe-card ${isSelected ? 'selected' : ''}`}>
      <div className="recipe-card-header">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={handleCheckboxChange}
          className="recipe-select-checkbox"
          aria-label={`Select ${recipe.name}`}
        />
        {recipe.image_url && (
          <img 
            src={recipe.image_url} 
            alt={recipe.name}
            className="recipe-image"
            onError={(e) => {
              (e.target as HTMLImageElement).style.display = 'none';
            }}
          />
        )}
      </div>
      
      <div className="recipe-card-content">
        <h3 className="recipe-title">
          <Link to={`/recipe/${recipe.id}`} className="recipe-link">
            {recipe.name}
          </Link>
        </h3>
        
        <div className="recipe-meta">
          <span className="recipe-time">
            ⏱️ {totalTime} min
          </span>
          {recipe.servings && (
            <span className="recipe-servings">
              👥 {recipe.servings} servings
            </span>
          )}
        </div>
        
        <div className="recipe-ingredients-preview">
          {recipe.recipe_ingredients.slice(0, 3).map((ri, index) => (
            <span key={ri.id} className="ingredient-tag">
              {ri.ingredient.name}
            </span>
          ))}
          {recipe.recipe_ingredients.length > 3 && (
            <span className="more-ingredients">
              +{recipe.recipe_ingredients.length - 3} more
            </span>
          )}
        </div>
        
        <div className="recipe-card-actions">
          <Link to={`/recipe/${recipe.id}`} className="btn btn-primary btn-sm">
            View Recipe
          </Link>
        </div>
      </div>
    </div>
  );
};

export default RecipeCard;