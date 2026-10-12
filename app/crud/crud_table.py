from sqlalchemy.orm import Session
from app.models.table import Table
from app.schemas.table import TableCreate


def get_table(db: Session, table_id: int):
    return db.query(Table).filter(Table.id == table_id).first()


def get_tables_by_restaurant(db: Session, restaurant_id: int):
    return db.query(Table).filter(Table.restaurant_id == restaurant_id).all()


def create_table(db: Session, table_in: TableCreate):
    db_table = Table(
        table_number=table_in.table_number,
        seats=table_in.seats,
        restaurant_id=table_in.restaurant_id,
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table