# Use Python 3.8 slim image for smaller footprint
FROM python:3.8-slim

# Set environment variables for optimal Python behavior
ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

# Install system dependencies in a single layer for efficiency
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  libjpeg-dev \
  zlib1g-dev \
  libfreetype6-dev \
  git \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
  && pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm /tmp/requirements.txt

# Set working directory
WORKDIR /workspace

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash vscode \
  && chown -R vscode:vscode /workspace
USER vscode