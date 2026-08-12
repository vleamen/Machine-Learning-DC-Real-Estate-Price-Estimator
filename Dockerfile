FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (libpq-dev for psycopg2, postgresql-client for pg_isready)
RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (app, scripts, CSV, etc.) into the container
COPY . .

# Expose the Flask port
EXPOSE 5000

# Use the entrypoint script to orchestrate startup
ENTRYPOINT ["./entrypoint.sh"]