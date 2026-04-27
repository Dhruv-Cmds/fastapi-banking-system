# Give me the image of python
FROM python:3.11-slim

# This means inside container all things work /app
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Dependecies '--no-catch-dir' This makes image short
RUN pip install --no-cache-dir -r requirements.txt

# Now copy whole project
COPY . .


# Expose port (fast api run on 8000 port)
EXPOSE 8000

# Run Fast Api "0.0.0.0" Allow outside access
CMD [ "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000" ]