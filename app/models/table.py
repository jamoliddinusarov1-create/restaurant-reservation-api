from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    restaurant_id = Column(
        Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False
    )

    restaurant = relationship("Restaurant", back_populates="tables")
    reservations = relationship(
        "Reservation", back_populates="table", cascade="all, delete-orphan"
    )