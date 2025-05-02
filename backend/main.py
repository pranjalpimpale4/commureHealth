from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quote_agent import get_random_quote  # <-- import this

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

@app.get("/quote")
def quote():
    try:
        text = get_random_quote()
        return {"quote": text}
    except Exception as e:
        return {"error": str(e)}
