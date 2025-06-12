FROM python:3.8-slim

ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

# Install build tools and Pillow dependencies, then clean up
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  libjpeg-dev \
  zlib1g-dev \
  libfreetype6-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip==20.3.4 setuptools==44.1.1 wheel==0.36.2 \
  && pip install --no-cache-dir -r /requirements.txt

WORKDIR /workspace