import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import type { GroceryList, GroceryListItem } from '../types';
import { groceryListAPI } from '../services/api';

const GroceryListPage = () => {
  const { id } = useParams<{ id?: string }>();
  const [groceryList, setGroceryList] = useState<GroceryList | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editingItems, setEditingItems] = useState<{ [key: string]: boolean }>({});
  const [editValues, setEditValues] = useState<{ [key: string]: { quantity: number; unit: string } }>({});

  useEffect(() => {
    if (id) {
      fetchGroceryList(id);
    }
  }, [id]);

  const fetchGroceryList = async (listId: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await groceryListAPI.getGroceryList(listId);
      setGroceryList(data);
      
      // Initialize edit values
      const initialEditValues: { [key: string]: { quantity: number; unit: string } } = {};
      data.items?.forEach(item => {
        initialEditValues[item.id] = {
          quantity: item.quantity,
          unit: item.unit
        };
      });
      setEditValues(initialEditValues);
    } catch (err) {
      setError('Failed to fetch grocery list');
      console.error('Error fetching grocery list:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartEdit = (itemId: string) => {
    setEditingItems(prev => ({ ...prev, [itemId]: true }));
  };

  const handleCancelEdit = (itemId: string) => {
    setEditingItems(prev => ({ ...prev, [itemId]: false }));
    // Reset edit values to original
    const originalItem = groceryList?.items?.find(item => item.id === itemId);
    if (originalItem) {
      setEditValues(prev => ({
        ...prev,
        [itemId]: {
          quantity: originalItem.quantity,
          unit: originalItem.unit
        }
      }));
    }
  };

  const handleSaveEdit = (itemId: string) => {
    // In a real app, this would make an API call to update the item
    console.log('Saving edit for item:', itemId, editValues[itemId]);
    
    // Update local state
    if (groceryList?.items) {
      const updatedItems = groceryList.items.map(item =>
        item.id === itemId
          ? { ...item, ...editValues[itemId] }
          : item
      );
      setGroceryList({ ...groceryList, items: updatedItems });
    }
    
    setEditingItems(prev => ({ ...prev, [itemId]: false }));
  };

  const handleEditValueChange = (itemId: string, field: 'quantity' | 'unit', value: string | number) => {
    setEditValues(prev => ({
      ...prev,
      [itemId]: {
        ...prev[itemId],
        [field]: value
      }
    }));
  };

  const handleDeleteItem = (itemId: string) => {
    if (confirm('Are you sure you want to remove this item?')) {
      // In a real app, this would make an API call
      console.log('Deleting item:', itemId);
      
      if (groceryList?.items) {
        const updatedItems = groceryList.items.filter(item => item.id !== itemId);
        setGroceryList({ ...groceryList, items: updatedItems });
      }
    }
  };

  const groupItemsByName = (items: GroceryListItem[]) => {
    const grouped: { [name: string]: GroceryListItem[] } = {};
    items.forEach(item => {
      const name = item.ingredient.name;
      if (!grouped[name]) {
        grouped[name] = [];
      }
      grouped[name].push(item);
    });
    return grouped;
  };

  if (!id) {
    return (
      <div className="grocery-list-page">
        <h1>Grocery Lists</h1>
        <div className="empty-state">
          <p>No grocery list selected.</p>
          <Link to="/" className="btn btn-primary">
            Go to Recipes
          </Link>
        </div>
      </div>
    );
  }

  if (loading) return <div className="loading">Loading grocery list...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!groceryList) return <div className="error">Grocery list not found</div>;

  const items = groceryList.items || [];
  const groupedItems = groupItemsByName(items);

  return (
    <div className="grocery-list-page">
      <div className="page-header">
        <nav className="breadcrumb">
          <Link to="/">← Back to Recipes</Link>
        </nav>
        <h1>Grocery List</h1>
      </div>

      {items.length === 0 ? (
        <div className="empty-state">
          <h2>Your grocery list is empty</h2>
          <p>Add some recipes to generate a grocery list!</p>
          <Link to="/" className="btn btn-primary">
            Browse Recipes
          </Link>
        </div>
      ) : (
        <div className="grocery-list-content">
          <div className="list-summary">
            <p>{items.length} item{items.length !== 1 ? 's' : ''} in your list</p>
          </div>

          <div className="grocery-items">
            {Object.entries(groupedItems)
              .sort(([a], [b]) => a.localeCompare(b))
              .map(([ingredientName, ingredientItems]) => (
              <div key={ingredientName} className="ingredient-group">
                <h3 className="ingredient-name">{ingredientName}</h3>
                <ul className="ingredient-items">
                  {ingredientItems.map(item => (
                    <li key={item.id} className="grocery-item">
                      {editingItems[item.id] ? (
                        <div className="edit-mode">
                          <input
                            type="number"
                            value={editValues[item.id]?.quantity || 0}
                            onChange={(e) => handleEditValueChange(item.id, 'quantity', Number(e.target.value))}
                            step="0.25"
                            min="0"
                            className="quantity-input"
                          />
                          <input
                            type="text"
                            value={editValues[item.id]?.unit || ''}
                            onChange={(e) => handleEditValueChange(item.id, 'unit', e.target.value)}
                            className="unit-input"
                          />
                          <div className="edit-actions">
                            <button
                              onClick={() => handleSaveEdit(item.id)}
                              className="btn btn-success btn-sm"
                            >
                              Save
                            </button>
                            <button
                              onClick={() => handleCancelEdit(item.id)}
                              className="btn btn-secondary btn-sm"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <div className="view-mode">
                          <span className="item-details">
                            <strong>{item.quantity} {item.unit}</strong>
                          </span>
                          <div className="item-actions">
                            <button
                              onClick={() => handleStartEdit(item.id)}
                              className="btn btn-secondary btn-sm"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleDeleteItem(item.id)}
                              className="btn btn-danger btn-sm"
                            >
                              Remove
                            </button>
                          </div>
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="list-actions">
            <Link to="/" className="btn btn-primary">
              Add More Recipes
            </Link>
            <button
              onClick={() => window.print()}
              className="btn btn-secondary"
            >
              Print List
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GroceryListPage;