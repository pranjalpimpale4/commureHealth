from fastapi import APIRouter
from agents.quote_agent import get_random_quote

quote_router = APIRouter()

@quote_router.get("/quote")
def quote():
    try:
        text = get_random_quote()
        return {"quote": text}
    except Exception as e:
        return {"error": str(e)}
