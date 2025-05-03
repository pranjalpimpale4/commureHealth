# README

---

## Prerequisites

- **Node.js** and **npm**
- **Python 3.10** or higher
- **pip**
- **virtualenv** (recommended)
- **SQLite** (optional; used by default)

---

## Frontend Setup

1. Navigate to the `frontend` folder:

cd frontend

2. Install dependencies:

npm install

3. Start the development server:

npm run dev


## Backend Setup

1. Navigate to the `backend` folder:

cd backend

2. Create a Python virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate

3. Install Python dependencies:

pip install -r requirements.txt

4. Start the FastAPI server:

uvicorn main:app --reload

## OR

If testing cron job along with apis: (Give permission to run shell script!)

./run_app_and_cron.sh

## Environment Variables
1. Create a .env file in the backend/ directory with the following content:

OPENAI_API_KEY=your-openai-api-key
Required for LLM features via CrewAI.

## Database Notes
Uses SQLite (hospital.db) by default.

Tables include InventoryItem, CommureEvent, etc.

You can modify or seed the database using SQLModel and available FastAPI routes.

To initiate the database with data:

cd backend

python insert_inventory.py

python insert_events.py
