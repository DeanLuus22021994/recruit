FROM python:3.8-slim

# Set environment variables for non-interactive installs and UTF-8
ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

# Install only essential build tools, clean up cache for smaller image
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel to legacy-compatible versions, then install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip==20.3.4 setuptools==44.1.1 wheel==0.36.2 \
  && pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace