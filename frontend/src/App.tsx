import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import HomePage from './pages/HomePage';
import RecipeViewPage from './pages/RecipeViewPage';
import CreateRecipePage from './pages/CreateRecipePage';
import GroceryListPage from './pages/GroceryListPage';
import MealPlanPage from './pages/MealPlanPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/recipe/:id" element={<RecipeViewPage />} />
            <Route path="/create-recipe" element={<CreateRecipePage />} />
            <Route path="/grocery-list/:id?" element={<GroceryListPage />} />
            <Route path="/meal-plan" element={<MealPlanPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
