from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.crud_reservation import (
    check_table_conflict,
    create_reservation,
    get_available_tables,
    get_reservation,
    get_user_reservations,
    update_reservation_status,
)
from app.crud.crud_table import get_table
from app.crud.crud_restaurant import get_restaurant
from app.models.user import User
from app.models.reservation import ReservationStatus
from app.schemas.reservation import (
    ReservationCreate,
    ReservationOut,
    ReservationUpdateStatus,
)
from app.schemas.table import TableOut

router = APIRouter()


@router.get("/available", response_model=List[TableOut])
def get_available_tables_endpoint(
    restaurant_id: int,
    start_time: datetime = Query(..., description="Format: YYYY-MM-DDTHH:MM:SS"),
    end_time: datetime = Query(..., description="Format: YYYY-MM-DDTHH:MM:SS"),
    db: Session = Depends(get_db),
):
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak.")
    
    return get_available_tables(db, restaurant_id=restaurant_id, start_time=start_time, end_time=end_time)


@router.post("/", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
def create_new_reservation(
    reservation_in: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if reservation_in.start_time >= reservation_in.end_time:
        raise HTTPException(status_code=400, detail="Vaqt oralig'i noto'g'ri kiritilgan.")
    
    table = get_table(db, table_id=reservation_in.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Stol topilmadi.")

    # Muhim qoida: Bir stol bir xil vaqtga ikki marta band qilinmasligi kerak
    has_conflict = check_table_conflict(
        db, 
        table_id=reservation_in.table_id, 
        start_time=reservation_in.start_time, 
        end_time=reservation_in.end_time
    )
    if has_conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu stol tanlangan vaqt oralig'ida allaqachon band qilingan!"
        )

    return create_reservation(db=db, reservation_in=reservation_in, user_id=current_user.id)


@router.get("/my", response_model=List[ReservationOut])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_reservations(db, user_id=current_user.id)


@router.patch("/{reservation_id}/status", response_model=ReservationOut)
def change_reservation_status(
    reservation_id: int,
    status_in: ReservationUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reservation = get_reservation(db, reservation_id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Bron topilmadi.")
    
    # Faqat o'zining bronini yoki admin o'zgartira olishi mumkin
    if reservation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Ruxsat etilmagan.")

    return update_reservation_status(db, reservation=reservation, status=status_in.status)