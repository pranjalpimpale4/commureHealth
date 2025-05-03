from fastapi import APIRouter
import json, os
from scripts.supply_agent_simulation import kickoff_negotiation

router = APIRouter()

@router.get("/chat-log")
def get_chat_log():
    log_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "chat_log.json")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            raw_logs = json.load(f)

        structured_logs = []
        round_num = 1
        for entry in raw_logs:
            if ":" in entry:
                role, content = entry.split(":", 1)
                structured_logs.append({
                    "round": round_num,
                    "role": role.strip(),
                    "content": content.strip()
                })
                round_num += 1
            else:
                structured_logs.append({
                    "round": round_num,
                    "role": "System",
                    "content": entry.strip()
                })
                round_num += 1

        return structured_logs
    return {"error": "Chat log not found."}


@router.post("/start-negotiation")
def start_negotiation():
    try:
        result = kickoff_negotiation()
        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
