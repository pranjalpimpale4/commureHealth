import sys
import os
import json
from datetime import datetime

# Add backend folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import CommureEvent
from db import get_session

# Correct path to events_data.json
json_path = os.path.join(os.path.dirname(__file__), "..", "data", "events_data.json")

# Load JSON data
with open(json_path, "r") as f:
    event_data = json.load(f)

# Insert into the database
with get_session() as session:
    for entry in event_data:
        event = CommureEvent(
            event_date=datetime.fromisoformat(entry["date"]).date(),
            category=entry["type"],
            count=entry["count"]
        )
        session.add(event)
    session.commit()
    print(f"Inserted {len(event_data)} events from {json_path}")
