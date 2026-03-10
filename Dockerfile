FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Presidio
RUN apt-get update && apt-get install -y gcc python3-dev

# Copy requirements first to cache them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the small Spacy model (Crucial step!)
RUN python -m spacy download en_core_web_sm

# Copy the application code
COPY app ./app

# Expose the port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]