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
    available_count: int
    threshold: int
