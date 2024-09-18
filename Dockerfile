# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# # Install system dependencies first
# RUN apt-get update && apt-get install -y libgl1-mesa-glx libxrender1 libxext6 libsm6
# Install necessary system dependencies for OpenCV and Gunicorn
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    libopencv-dev \
    wget

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install YOLOv8
RUN pip install ultralytics
# Download YOLOv8 model
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
# Create necessary directories
RUN mkdir -p /app/logs /app/outputs /app/yolov8

# Copy the rest of the application
COPY . /app

# Create necessary directories
RUN mkdir -p /app/logs /app/outputs

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
