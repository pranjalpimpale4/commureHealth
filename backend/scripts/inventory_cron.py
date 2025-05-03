import time
import requests
import schedule

def run_inventory_check():
    try:
        response = requests.get("http://127.0.0.1:8000/inventory/adjust-threshold")
        print("Inventory check response:", response.json())
    except Exception as e:
        print("Error in inventory check:", e)

# Run once immediately for testing
print("Running immediate test check...")
run_inventory_check()

# Schedule to run every 7 days
schedule.every(7).days.do(run_inventory_check)

print("Scheduler started... Running every 7 days")
while True:
    schedule.run_pending()
    time.sleep(60)
