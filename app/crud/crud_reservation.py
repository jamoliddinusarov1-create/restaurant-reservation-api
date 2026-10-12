from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.reservation import ReservationCreate


def check_table_conflict(db: Session, table_id: int, start_time: datetime, end_time: datetime):
    """
    Berilgan stol ko'rsatilgan vaqt oralig'ida allaqachon band qilinganligini tekshiradi.
    Qoidaga ko'ra: yangi bronning start vaqti eskining end vaqtidan oldin tugasa 
    va yangining end vaqti eskining start vaqtidan keyin boshlansa - to'qnashuv bor.
    """
    conflict = db.query(Reservation).filter(
        Reservation.table_id == table_id,
        Reservation.status == ReservationStatus.CONFIRMED,
        and_(
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        )
    ).first()
    return conflict is not None


def get_reservation(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()


def get_user_reservations(db: Session, user_id: int):
    return db.query(Reservation).filter(Reservation.user_id == user_id).all()


def get_available_tables(db: Session, restaurant_id: int, start_time: datetime, end_time: datetime):
    from app.models.table import Table
    # Barcha stollarni olamiz
    all_tables = db.query(Table).filter(Table.restaurant_id == restaurant_id).all()
    
    available = []
    for table in all_tables:
        has_conflict = check_table_conflict(db, table.id, start_time, end_time)
        if not has_conflict:
            available.append(table)
    return available


def create_reservation(db: Session, reservation_in: ReservationCreate, user_id: int):
    db_reservation = Reservation(
        user_id=user_id,
        table_id=reservation_in.table_id,
        start_time=reservation_in.start_time,
        end_time=reservation_in.end_time,
        status=ReservationStatus.CONFIRMED
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def update_reservation_status(db: Session, reservation: Reservation, status: ReservationStatus):
    reservation.status = status
    db.commit()
    db.refresh(reservation)
    return reservation