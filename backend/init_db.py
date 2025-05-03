
# scripts/init_db.py
from sqlmodel import SQLModel
from db import engine
from models import InventoryItem  # include all your models

SQLModel.metadata.create_all(engine)
print("✅ Database and tables created")
