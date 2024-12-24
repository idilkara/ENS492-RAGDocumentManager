
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall bson
# Copy the rest 
COPY . .

# Expose the port app runs on
EXPOSE 8080

CMD ["python3", "app.py"]
