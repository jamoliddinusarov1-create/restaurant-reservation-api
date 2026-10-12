from pydantic import BaseModel


class TableBase(BaseModel):
    table_number: str
    seats: int


class TableCreate(TableBase):
    restaurant_id: int


class TableOut(TableBase):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True