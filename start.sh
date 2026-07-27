#!/bin/bash
# Startup script for Railway deployment

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

echo "Starting FastAPI server on port $PORT"
exec python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
