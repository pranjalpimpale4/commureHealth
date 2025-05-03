import math
from sqlmodel import Session, select
from models import InventoryItem

class InventoryAssessor:
    def __init__(self, session: Session, safety_margin: float = 1.1):
        self.session = session
        self.safety_margin = safety_margin

    def get_inventory(self):
        return self.session.exec(select(InventoryItem)).all()

    def get_understocked_items(self):
        inventory = self.get_inventory()
        understocked = []
        for item in inventory:
            if item.available_count < item.threshold:
                needed_qty = math.ceil((item.threshold - item.available_count) * self.safety_margin)
                understocked.append({
                    "item_id": item.id,
                    "item": item.name,
                    "needed": needed_qty
                })
        return understocked
