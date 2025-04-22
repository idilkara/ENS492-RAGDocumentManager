
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

# Install dependencies
RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest 
COPY . .

# Expose the port app runs on
EXPOSE 8080

CMD ["python3", "app.py"]
