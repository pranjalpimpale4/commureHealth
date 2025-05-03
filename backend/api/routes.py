from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import CommureEvent, InventoryItem
from db import get_session
import json
from datetime import date
from datetime import date, timedelta
import os
router = APIRouter()



@router.get("/check-inventory")
def check_inventory(session: Session = Depends(get_session)):
    base_dir = os.path.dirname(os.path.dirname(__file__))  # goes from api/ to backend/
    json_path = os.path.join(base_dir, "data", "category_mapping.json")

    with open(json_path) as f:
        category_map = json.load(f)
    
    # ... rest of the function


    today = date.today()
    one_month_later = today + timedelta(days=30)

    # Query upcoming events
    events = session.exec(
        select(CommureEvent).where(
            CommureEvent.event_date >= today,
            CommureEvent.event_date <= one_month_later
        )
    ).all()

    # item_id -> total quantity needed
    item_requirements = {}

    for event in events:
        mappings = category_map.get(event.category.lower(), [])
        for mapping in mappings:
            item_id = mapping["item_id"]
            coef = mapping["coefficient"]
            item_requirements[item_id] = item_requirements.get(item_id, 0) + (coef * event.count)

    # Check against inventory
    shortages = []

    for item_id, needed in item_requirements.items():
        inventory = session.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
        if inventory:
            to_order = max(0, needed - inventory.available_count)
            if to_order > 0:
                shortages.append({
                    "item_id": item_id,
                    "item": inventory.name,
                    "needed": needed,
                    "available": inventory.available_count,
                    "to_order": to_order
                })
        else:
            shortages.append({
                "item_id": item_id,
                "item": None,
                "needed": needed,
                "available": 0,
                "to_order": needed
            })

    return {"shortages": shortages}
