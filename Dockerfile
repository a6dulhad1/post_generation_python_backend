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
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p data/images data/generated logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port for dashboard (optional)
EXPOSE 5000

# Default command
CMD ["python", "main.py", "--mode", "auto"]
