FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Railway provides PORT env variable
ENV PORT=8080

# Run the application using shell form to expand $PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
