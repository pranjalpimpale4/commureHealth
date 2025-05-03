from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import CommureEvent, InventoryItem, Order
from db import get_session
import json
from datetime import date
from datetime import date, timedelta
import os
from fastapi import FastAPI
app = FastAPI()
router = APIRouter()
from agents.appointment_forecaster import run_forecast
from fastapi.responses import JSONResponse
from datetime import datetime
from agents.disaster_inventory_agent import run_disaster_inventory_agent  # ✅ Step 3 agent import
from tools.fetch_disasters import  DisasterFetcher


from . import chat
app.include_router(chat.router)



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

def compute_inventory_shortages(events, category_map, session: Session):
    item_requirements = {}

    for event in events:
        mappings = category_map.get(event["category"].lower(), [])
        for mapping in mappings:
            item_id = mapping["item_id"]
            coef = mapping["coefficient"]
            item_requirements[item_id] = item_requirements.get(item_id, 0) + (coef * event["count"])

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
    return shortages

@router.post("/forecast/run-now")
def run_forecast_now(session: Session = Depends(get_session)):
    try:
        # Run Prophet forecast
        result = run_forecast()
        forecast_events = result["forecast"]

        # Prepare events for shortage calculator
        processed_events = []
        for f in forecast_events:
            processed_events.append({
                "category": f["category"],
                "event_date": datetime.strptime(f["event_date"], "%Y-%m-%d").date(),
                "count": f["count"]
            })

        # Load category mapping
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mapping_path = os.path.join(base_dir, "data", "category_mapping.json")
        with open(mapping_path) as f:
            category_map = json.load(f)

        # Compute inventory shortages based on forecast
        shortages = compute_inventory_shortages(processed_events, category_map, session)

        return {
            "status": "success",
            "message": "Forecast generated and inventory checked successfully",
            "generated_on": result["generated_on"],
            "forecast_count": len(forecast_events),
            "forecast": forecast_events,
            "shortages": shortages
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

# @router.post("/inventory/adjust-threshold")
# def adjust_inventory_thresholds(session: Session = Depends(get_session)):
#     try:
#         # Load mapping file
#         base_dir = os.path.dirname(os.path.dirname(__file__))
#         mapping_path = os.path.join(base_dir, "data", "category_mapping.json")
#         with open(mapping_path) as f:
#             category_map = json.load(f)

#         # ========== 1. Get DB Events ========== #
#         today = date.today()
#         one_month_later = today + timedelta(days=30)

#         db_events = session.exec(
#             select(CommureEvent).where(
#                 CommureEvent.event_date >= today,
#                 CommureEvent.event_date <= one_month_later
#             )
#         ).all()

#         # Prepare DB events
#         db_event_data = [
#             {"category": event.category, "event_date": event.event_date, "count": event.count}
#             for event in db_events
#         ]

#         db_shortages = compute_inventory_shortages(db_event_data, category_map, session)

#         # ========== 2. Run Forecast ========== #
#         result = run_forecast()
#         forecast_event_data = [
#             {
#                 "category": f["category"],
#                 "event_date": datetime.strptime(f["event_date"], "%Y-%m-%d").date(),
#                 "count": f["count"]
#             }
#             for f in result["forecast"]
#         ]

#         forecast_shortages = compute_inventory_shortages(forecast_event_data, category_map, session)

#         # ========== 3. Compare Shortages ========== #
#         max_needed_by_item = {}

#         for shortage in db_shortages + forecast_shortages:
#             item_id = shortage["item_id"]
#             needed = shortage["needed"]
#             max_needed_by_item[item_id] = max(max_needed_by_item.get(item_id, 0), needed)

#         # ========== 4. Update Inventory Thresholds ========== #
#         updated_items = []

#         for item_id, new_threshold in max_needed_by_item.items():
#             inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
#             if inventory_item and inventory_item.threshold != new_threshold:
#                 inventory_item.threshold = new_threshold
#                 session.add(inventory_item)
#                 updated_items.append({
#                     "item_id": item_id,
#                     "item": inventory_item.name,
#                     "new_threshold": new_threshold
#                 })

#         session.commit()

#         return {
#             "status": "success",
#             "message": f"{len(updated_items)} thresholds updated",
#             "updates": updated_items
#         }

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"status": "error", "message": str(e)}
#         )

from fastapi.responses import JSONResponse

@router.post("/inventory/adjust-threshold")
def adjust_inventory_thresholds(session: Session = Depends(get_session)):
    try:
        # Load mapping file
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mapping_path = os.path.join(base_dir, "data", "category_mapping.json")
        with open(mapping_path) as f:
            category_map = json.load(f)

        # ========== 1. Get DB Events ========== #
        today = date.today()
        one_month_later = today + timedelta(days=30)

        db_events = session.exec(
            select(CommureEvent).where(
                CommureEvent.event_date >= today,
                CommureEvent.event_date <= one_month_later
            )
        ).all()

        db_event_data = [
            {"category": event.category, "event_date": event.event_date, "count": event.count}
            for event in db_events
        ]

        db_shortages = compute_inventory_shortages(db_event_data, category_map, session)
        print("\n📦 DB-Driven Shortages:")
        for item in db_shortages:
            print(item)

        # ========== 2. Run Forecast ========== #
        result = run_forecast()
        forecast_event_data = [
            {
                "category": f["category"],
                "event_date": datetime.strptime(f["event_date"], "%Y-%m-%d").date(),
                "count": f["count"]
            }
            for f in result["forecast"]
        ]

        forecast_shortages = compute_inventory_shortages(forecast_event_data, category_map, session)
        print("\n📈 Forecast-Based Shortages:")
        for item in forecast_shortages:
            print(item)

        # ========== 3. AI Agent Recommendations ========== #
        ai_shortages = run_disaster_inventory_agent()
        print("\n🤖 AI Agent Recommendations:")
        for item in ai_shortages:
            print(item)

        # ========== 4. Compare All Shortages ========== #
        max_needed_by_item = {}

        for source in [db_shortages, forecast_shortages, ai_shortages]:
            for shortage in source:
                item_id = shortage["item_id"]
                needed = shortage["needed"]
                max_needed_by_item[item_id] = max(max_needed_by_item.get(item_id, 0), needed)

        print("\n✅ Final Max Needed by Item (Before DB Update):")
        for item_id, needed in max_needed_by_item.items():
            print(f"Item ID: {item_id}, Max Needed: {needed}")

        # ========== 5. Update Inventory Thresholds ========== #
        updated_items = []

        for item_id, new_threshold in max_needed_by_item.items():
            inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
            if inventory_item and inventory_item.threshold != new_threshold:
                inventory_item.threshold = new_threshold
                session.add(inventory_item)
                updated_items.append({
                    "item_id": item_id,
                    "item": inventory_item.name,
                    "new_threshold": new_threshold
                })


        # ========== 6. Generate Orders for Items Below Threshold ========== #
        created_orders = []

        for item in updated_items:
            inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == item["item_id"])).first()
            if inventory_item and inventory_item.threshold > inventory_item.available_count:
                quantity_to_order = inventory_item.threshold - inventory_item.available_count
                new_order = Order(
                    item_id=inventory_item.id,
                    name=inventory_item.name,
                    item_description=f"Auto-generated order for {inventory_item.name}",
                    no_of_ordered_items=quantity_to_order,
                    status="pending"
                )
                session.add(new_order)
                created_orders.append({
                    "item_id": inventory_item.id,
                    "item": inventory_item.name,
                    "ordered": quantity_to_order,
                    "status": "pending"
                })


        session.commit()

        return {
            "status": "success",
            "message": f"{len(updated_items)} thresholds updated",
            "updates": updated_items,
            "orders": created_orders
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.get("/inventory/list")
def get_inventory(session: Session = Depends(get_session)):
    try:
        items = session.exec(select(InventoryItem)).all()
        response = []

        for item in items:
            status = "Sufficient"
            if item.available_count < item.threshold:
                status = "Low Stock"
            elif item.available_count == 0:
                status = "Out of Stock"

            response.append({
                "item_id": item.id,
                "name": item.name,
                "available_count": item.available_count,
                "threshold": item.threshold,
                "status": status
            })

        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

from fastapi import Body

@router.post("/inventory/create")
def create_inventory_item(
    name: str = Body(...),
    available_count: int = Body(...),
    threshold: int = Body(...),
    session: Session = Depends(get_session)
):
    try:
        new_item = InventoryItem(
            name=name,
            available_count=available_count,
            threshold=threshold
        )
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
        return {
            "status": "success",
            "message": "Inventory item created",
            "item": {
                "item_id": new_item.id,
                "name": new_item.name,
                "available_count": new_item.available_count,
                "threshold": new_item.threshold
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.delete("/inventory/delete/{item_id}")
def delete_inventory_item(item_id: int, session: Session = Depends(get_session)):
    try:
        item = session.get(InventoryItem, item_id)
        if not item:
            return {"status": "error", "message": "Item not found"}

        session.delete(item)
        session.commit()
        return {"status": "success", "message": f"Item {item_id} deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/inventory/shortages/disaster")
def get_disaster_based_shortages(session: Session = Depends(get_session)):
    try:
        # Load category mapping
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mapping_path = os.path.join(base_dir, "data", "category_mapping.json")
        with open(mapping_path) as f:
            category_map = json.load(f)

        # Run AI disaster inventory agent
        ai_shortages = run_disaster_inventory_agent()

        fetcher = DisasterFetcher()
        disasters = fetcher.get_disasters()
        headlines = [d["headline"] for d in disasters if d.get("headline")]



        # Build response
        response = []
        for shortage in ai_shortages:
            item_id = shortage["item_id"]
            needed = shortage["needed"]
            inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
            response.append({
                "item_id": item_id,
                "item": inventory_item.name if inventory_item else "Unknown",
                "description": inventory_item.description if inventory_item else "N/A",
                "available": inventory_item.available_count if inventory_item else 0,
                "needed": needed
            })

        return {
            "status": "success",
            "source": "disaster_agent",
            "Event": headlines[:10],
            "shortages": response
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.post("/inventory/shortages/forecast")
def get_forecast_based_shortages(session: Session = Depends(get_session)):
    try:
        # Load category mapping
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mapping_path = os.path.join(base_dir, "data", "category_mapping.json")
        with open(mapping_path) as f:
            category_map = json.load(f)

        # Run Prophet forecast
        result = run_forecast()
        forecast_events = [
            {
                "category": f["category"],
                "event_date": datetime.strptime(f["event_date"], "%Y-%m-%d").date(),
                "count": f["count"]
            }
            for f in result["forecast"]
        ]

        # Compute shortages
        shortages = compute_inventory_shortages(forecast_events, category_map, session)

        # Build response
        response = []
        for shortage in shortages:
            item_id = shortage["item_id"]
            needed = shortage["needed"]
            inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
            response.append({
                "item_id": item_id,
                "item": inventory_item.name if inventory_item else "Unknown",
                "description": inventory_item.description if inventory_item else "N/A",
                "available": inventory_item.available_count if inventory_item else 0,
                "needed": needed
            })

        return {
            "status": "success",
            "source": "forecast_model",
            "shortages": response
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
