
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies & clean up to save space
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies without caching wheels
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest 
COPY . .

# Expose the port app runs on
EXPOSE 8080

CMD ["python3", "app.py"]
