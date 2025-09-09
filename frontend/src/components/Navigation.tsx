import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <h1>Meal Planner</h1>
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              Recipes
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/create-recipe" className="nav-link">
              Create Recipe
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/grocery-list" className="nav-link">
              Grocery List
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;