#!/bin/bash
echo "Starting FastAPI server..."
uvicorn main:app --reload &
sleep 120  # or 30s if needed
echo "Starting cron job..."
python3 scripts/inventory_cron.py
