# Use Python with playwright pre-installed browsers
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8000
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000

# Run the API server
CMD ["python", "-m", "src.api"]

