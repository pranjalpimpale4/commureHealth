from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class CommureEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_date: date
    category: str
    count: int

class InventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None  # ✅ Add this line
    available_count: int
    threshold: int

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int
    name: str
    item_description: str
    no_of_ordered_items: int
    status: str