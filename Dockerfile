# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY backend/ /app/backend/

# Set the working directory to where manage.py is
WORKDIR /app/backend

# Expose the port the app runs on
EXPOSE 8000

# Run migrations and initialization, then start the application
CMD ["sh", "-c", "python manage.py migrate && python init_admin.py && python manage.py runserver 0.0.0.0:8000"]
