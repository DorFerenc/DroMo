# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install necessary system dependencies for OpenCV and Gunicorn
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    libopencv-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create directory for YOLOv3 files
# RUN mkdir -p /app/yolov3

# Download YOLOv3 files
# RUN mkdir -p /app/app/yolov3
# RUN wget -O /app/app/yolov3/yolov3.weights https://pjreddie.com/media/files/yolov3.weights
# RUN wget -O /app/app/yolov3/yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
# RUN wget -O /app/app/yolov3/coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
# Download YOLO weights, config, and COCO dataset labels
# RUN curl -o /app/yolov3.weights https://pjreddie.com/media/files/yolov3.weights
# RUN curl -o /app/yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
# RUN curl -o /app/coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]