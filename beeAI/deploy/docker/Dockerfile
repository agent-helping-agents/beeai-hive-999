FROM python:3.12-slim

# Security: Run as non-root
RUN groupadd -r beeai && useradd -r -g beeai beeai

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Set permissions
RUN chown -R beeai:beeai /app

# Switch to non-root user
USER beeai

# Expose ports
EXPOSE 22181 22182

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:22181/health')" || exit 1

# Start command
CMD ["python", "-m", "src.api.secure_server_fixed"]
