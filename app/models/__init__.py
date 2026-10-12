from app.core.config import settings
from app.core.database import Base

# Barcha modellarni shu yerda aniq import qilamiz
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.table import Table
from app.models.reservation import Reservation

target_metadata = Base.metadata