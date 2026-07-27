# Dockerfile for AI Social Media Automation System
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_api.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p data/images data/generated logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port for API
EXPOSE ${PORT}

# Start FastAPI server (use shell form to expand $PORT variable)
CMD python -m uvicorn api.main:app --host 0.0.0.0 --port ${PORT}
