from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def get_restaurant(db: Session, restaurant_id: int):
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Restaurant).offset(skip).limit(limit).all()


def create_restaurant(db: Session, restaurant_in: RestaurantCreate):
    db_restaurant = Restaurant(
        name=restaurant_in.name,
        description=restaurant_in.description,
        address=restaurant_in.address,
        phone_number=restaurant_in.phone_number,
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant