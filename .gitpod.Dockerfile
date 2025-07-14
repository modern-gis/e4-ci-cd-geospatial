FROM python:3.11-slim

# Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      gdal-bin libgdal-dev \
      git \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install \
      apache-airflow==3.0.1 \
      apache-airflow-providers-http \
      pytest \
      flake8 \
      requests \
      geopandas \
      fiona \
      pyproj \
      flask-session

EXPOSE 8080
CMD ["bash"]
