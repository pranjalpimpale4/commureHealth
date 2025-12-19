import sys
import os
import json
from sqlmodel import delete  # ✅ Import delete for SQLModel

# Add backend folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import InventoryItem
from db import get_session

# Path to the JSON file
json_path = os.path.join(os.path.dirname(__file__), "..", "data", "inventory_items.json")

# Load JSON data
with open(json_path, "r") as f:
    items_data = json.load(f)

# Clear old records and insert new ones
with get_session() as session:
    # ✅ Step 1: Delete all existing records using SQLModel recommended approach
    session.exec(delete(InventoryItem))

    # ✅ Step 2: Insert new records
    for entry in items_data:
        item = InventoryItem(
            name=entry["name"],
            description=entry["description"],
            available_count=entry["available_count"],
            threshold=entry["threshold"]
        )
        session.add(item)

    session.commit()
    print(f"✅ Reset complete: {len(items_data)} inventory items inserted from {json_path}")
