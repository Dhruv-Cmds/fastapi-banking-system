# Give me the image of python
FROM python:3.11-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# This means inside container all things work /app
WORKDIR /app


# Copy requirements.txt
COPY requirements.txt .


# Install Dependecies '--no-cache-dir' This makes image short
RUN pip install --no-cache-dir -r requirements.txt


# Now copy whole project
COPY . .


# Expose port (fast api run on 8000 port)
EXPOSE 8000


# Run Fast Api "0.0.0.0" Allow outside access
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# when prod use this 
# CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]