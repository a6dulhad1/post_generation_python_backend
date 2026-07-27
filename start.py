#!/usr/bin/env python3
"""Startup script for Railway deployment"""
import os
import sys

# Get PORT from environment variable, default to 8000
port = os.environ.get("PORT", "8000")

print(f"Starting FastAPI server on port {port}")

# Run uvicorn
os.execvp("python", [
    "python", "-m", "uvicorn",
    "api.main:app",
    "--host", "0.0.0.0",
    "--port", port
])
