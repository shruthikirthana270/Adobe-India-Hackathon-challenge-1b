# Use Python 3.10 slim image for smaller size
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PDF processing and ML libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libssl-dev \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to latest version
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install Python dependencies with optimizations
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copy the processing script and other files
COPY process_collections.py .
COPY validate_outputs.py .

# Create necessary directories with proper permissions
RUN mkdir -p /app/Challenge_1b && \
    chmod -R 755 /app

# Set environment variables for better performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set permissions for scripts
RUN chmod +x process_collections.py validate_outputs.py

# Run the collection processor
CMD ["python", "process_collections.py"]
