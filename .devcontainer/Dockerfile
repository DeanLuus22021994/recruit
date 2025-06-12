FROM mcr.microsoft.com/devcontainers/python:1-3.8-bullseye

# Install system dependencies (minimal for performance)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/*


# Install Python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace
