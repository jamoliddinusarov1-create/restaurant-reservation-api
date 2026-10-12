from datetime import datetime
from pydantic import BaseModel
from app.models.reservation import ReservationStatus


class ReservationCreate(BaseModel):
    table_id: int
    start_time: datetime
    end_time: datetime


class ReservationUpdateStatus(BaseModel):
    status: ReservationStatus


class ReservationOut(BaseModel):
    id: int
    user_id: int
    table_id: int
    start_time: datetime
    end_time: datetime
    status: ReservationStatus

    class Config:
        from_attributes = True