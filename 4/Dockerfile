# Use official Python image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    python3-distutils \
    gfortran \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./main.py"]
