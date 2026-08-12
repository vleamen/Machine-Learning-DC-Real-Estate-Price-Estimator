# Use a slim Python image to keep the container lightweight
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for psycopg2 and compiling ML libraries
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy requirements and install them
# (Make sure to create a requirements.txt with flask, pandas, scikit-learn, sqlalchemy, psycopg2-binary, joblib)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app and the serialized model artifact
COPY app.py .
COPY dc_model.pkl .

# Expose the Flask port
EXPOSE 5000

# Command to run the API
CMD ["flask", "run", "--host=0.0.0.0"]