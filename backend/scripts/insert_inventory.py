import sys
import os
import json

# Add backend folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import InventoryItem
from db import get_session

# Correct path to inventory_items.json
json_path = os.path.join(os.path.dirname(__file__), "..", "data", "inventory_items.json")

# Load JSON data
with open(json_path, "r") as f:
    items_data = json.load(f)

# Insert into the database
with get_session() as session:
    for entry in items_data:
        item = InventoryItem(
            name=entry["name"],
            description=entry["description"],
            available_count=entry["available_count"],
            threshold=entry["threshold"]
        )
        session.add(item)
    session.commit()
    print(f"Inserted {len(items_data)} inventory items from {json_path}")
