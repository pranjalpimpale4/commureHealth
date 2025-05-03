from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import CommureEvent, InventoryItem
from db import get_session
import json
from datetime import date

router = APIRouter()

@router.get("/check-inventory/{event_date}")
def check_inventory(event_date: date, session: Session = Depends(get_session)):
    with open("category_mapping.json") as f:
        category_map = json.load(f)

    events = session.exec(select(CommureEvent).where(CommureEvent.event_date == event_date)).all()

    shortages = []
    for event in events:
        items_needed = category_map.get(event.category, [])
        for item in items_needed:
            inventory = session.exec(select(InventoryItem).where(InventoryItem.name == item)).first()
            if inventory:
                required = event.count
                if inventory.available_count < required:
                    shortages.append({
                        "item": item,
                        "needed": required,
                        "available": inventory.available_count,
                        "status": "Order Required"
                    })
            else:
                shortages.append({
                    "item": item,
                    "needed": event.count,
                    "available": 0,
                    "status": "Item Not Found"
                })

    return {"shortages": shortages}
