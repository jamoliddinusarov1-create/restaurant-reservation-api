from fastapi import APIRouter
from app.api.v1.endpoints import auth, restaurants, tables, reservations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])
api_router.include_router(tables.router, prefix="/tables", tags=["Tables"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])