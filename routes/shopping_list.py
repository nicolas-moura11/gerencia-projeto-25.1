'''

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ShoppingListItem
from security import get_current_user, get_db
from models import ShoppingListItemCreate, ShoppingListItemRead

router = APIRouter()

@router.post("/shopping-list", response_model=ShoppingListItemRead)
def add_item(item: ShoppingListItemCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_item = ShoppingListItem(**item.dict(), user_id=user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/shopping-list", response_model=list[ShoppingListItemRead])
def get_items(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(ShoppingListItem).filter_by(user_id=user.id).all()

@router.delete("/shopping-list/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    item = db.query(ShoppingListItem).filter_by(id=item_id, user_id=user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Item removido com sucesso"}
'''
