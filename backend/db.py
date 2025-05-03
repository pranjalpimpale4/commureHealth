import os
from sqlmodel import SQLModel, create_engine, Session

# Make DB path relative to the file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
