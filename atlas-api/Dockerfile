# Use the official Python image from Docker Hub (pickledb>=1.4 needs Python 3.10+)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the local api directory into the container at /app
COPY api/ /app/api/

# Set environment variables
ENV PYTHONPATH=/app

# Command to run the FastAPI application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

