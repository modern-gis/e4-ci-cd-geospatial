# File: .gitpod.Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      gdal-bin libgdal-dev \
      git \
    && rm -rf /var/lib/apt/lists/*

# GDAL environment (for Python wheels)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set workdir
WORKDIR /workspace

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install \
      apache-airflow==2.8.1 \
      apache-airflow-providers-http \
      pytest \
      flake8 \
      requests \
      geopandas \
      fiona \
      pyproj

# Expose Airflow webserver port (if you choose to start it)
EXPOSE 8080

# Default command: open a bash shell
CMD [ "bash" ]
