from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser
from app.core.database import get_db
from app.crud.crud_restaurant import get_restaurant
from app.crud.crud_table import create_table, get_tables_by_restaurant
from app.models.user import User
from app.schemas.table import TableCreate, TableOut

router = APIRouter()


@router.get("/restaurant/{restaurant_id}", response_model=List[TableOut])
def list_restaurant_tables(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restoran topilmadi.")
    return get_tables_by_restaurant(db, restaurant_id=restaurant_id)


@router.post("/", response_model=TableOut, status_code=status.HTTP_201_CREATED)
def add_table(
    table_in: TableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    restaurant = get_restaurant(db, restaurant_id=table_in.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Ko'rsatilgan restoran topilmadi.")
    return create_table(db=db, table_in=table_in)