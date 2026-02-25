# Use standard Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the app with New Relic APM
CMD ["newrelic-admin", "run-program", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]