from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.grocery_list import GroceryList
from app.services.grocery_list import build_grocery_list
from app.repositories.grocery_list import get_grocery_list
from pydantic import BaseModel

router = APIRouter()

class CreateGroceryListRequest(BaseModel):
    recipe_ids: List[UUID]

@router.post("/grocery-lists/", response_model=GroceryList)
def create_grocery_list_from_recipes(
    request: CreateGroceryListRequest, 
    db: Session = Depends(get_db)
):
    """Create a grocery list from a list of recipe IDs"""
    if not request.recipe_ids:
        raise HTTPException(status_code=400, detail="At least one recipe ID is required")
    
    try:
        grocery_list = build_grocery_list(db, request.recipe_ids)
        return grocery_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create grocery list: {str(e)}")

@router.get("/grocery-lists/{grocery_list_id}", response_model=GroceryList)
def get_grocery_list_by_id(
    grocery_list_id: UUID, 
    db: Session = Depends(get_db)
):
    """Get a grocery list by its ID"""
    grocery_list = get_grocery_list(db, grocery_list_id)
    if grocery_list is None:
        raise HTTPException(status_code=404, detail="Grocery list not found")
    return grocery_list