from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from api.routes import router as inventory_router
from api.hello import hello_router
from api.quote import quote_router

# backend/main.py
from fastapi import FastAPI
from api import routes

from api import chat



app = FastAPI()
app.include_router(routes.router)
app.include_router(chat.router)

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router)
app.include_router(hello_router)
app.include_router(quote_router)
