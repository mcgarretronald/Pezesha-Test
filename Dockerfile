# Use the official Python image as a base
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files to disk and to ensure it uses UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (for handling dependencies and running the app)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port that Django will run on (default is 8000)
EXPOSE 8000

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
