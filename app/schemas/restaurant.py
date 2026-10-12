from typing import Optional
from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    phone_number: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    name: Optional[str] = None
    address: Optional[str] = None


class RestaurantOut(RestaurantBase):
    id: int

    class Config:
        from_attributes = True