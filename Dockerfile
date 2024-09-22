# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    FLASK_APP=run.py \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    build-essential \
    libpng-dev \
    libjpeg-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install OpenCV separately
RUN wget -O opencv.deb http://security.debian.org/debian-security/pool/updates/main/o/opencv/libopencv-dev_3.2.0+dfsg-6+deb10u1_amd64.deb \
    && dpkg -i opencv.deb || true \
    && apt-get update \
    && apt-get -f install -y \
    && rm opencv.deb \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Create necessary directories
RUN mkdir -p logs outputs

# Create a non-root user
RUN useradd --create-home appuser
USER appuser

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]