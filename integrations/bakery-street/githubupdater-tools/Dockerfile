FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_poly.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_poly.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs config examples tests

# Make scripts executable
RUN chmod +x *.sh *.py

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port for dashboard
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import poly_framework; print('OK')" || exit 1

# Default command
CMD ["python3", "poly_framework.py"]
