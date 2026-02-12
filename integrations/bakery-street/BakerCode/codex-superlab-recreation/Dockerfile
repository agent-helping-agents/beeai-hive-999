FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create templates directory
RUN mkdir -p templates

# Expose port
EXPOSE 8000

# Default command (can be overridden)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_dashboard:app"]