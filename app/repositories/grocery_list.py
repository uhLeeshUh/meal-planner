from sqlalchemy.orm import Session, joinedload
from app.schemas.grocery_list import GroceryListCreate
from app.models.grocery_list import GroceryList
from app.models.grocery_list_item import GroceryListItem

def create_grocery_list(db: Session, grocery_list_create: GroceryListCreate):
    # first create a grocery list 
    grocery_list = GroceryList()
    db.add(grocery_list)
    db.flush()  # Get the grocery list ID

    # then create the items, associated with grocery list
    for item in grocery_list_create.items:
        gl_item = GroceryListItem(grocery_list_id=grocery_list.id, ingredient_id=item.ingredient_id, quantity=item.total_quantity, unit=item.unit)
        db.add(gl_item)

    # then close transaction and return
    db.commit()

    # Eager load items to the grocery list
    grocery_list = db.query(GroceryList).options(joinedload(GroceryList.items)).get(grocery_list.id)
    return grocery_list
