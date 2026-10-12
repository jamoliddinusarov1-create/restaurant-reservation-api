from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.crud.crud_restaurant import create_restaurant, get_restaurant, get_restaurants
from app.models.user import User
from app.schemas.restaurant import RestaurantCreate, RestaurantOut

router = APIRouter()


@router.get("/", response_model=List[RestaurantOut])
def list_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_restaurants(db, skip=skip, limit=limit)


@router.post("/", response_model=RestaurantOut, status_code=status.HTTP_201_CREATED)
def add_restaurant(
    restaurant_in: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return create_restaurant(db=db, restaurant_in=restaurant_in)


@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant_detail(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restoran topilmadi.")
    return restaurant