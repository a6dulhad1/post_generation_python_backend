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

# Copy startup script
COPY start.py /app/start.py

# Expose port for API
EXPOSE 8000

# Start FastAPI server using Python startup script
CMD ["python", "/app/start.py"]
