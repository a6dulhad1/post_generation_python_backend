#!/bin/bash

echo "================================================"
echo "Starting AI Social Media API Server"
echo "================================================"
echo ""

# Install dependencies if needed
echo "Checking dependencies..."
pip install -r requirements_api.txt --quiet

# Create necessary directories
mkdir -p data/images

# Start the API server
echo ""
echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "API Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
