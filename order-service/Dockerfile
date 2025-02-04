# order-service/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code.
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]