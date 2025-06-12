FROM mcr.microsoft.com/devcontainers/python:1-3.8-bullseye


# Install only essential build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*




# Pin pip, setuptools, and wheel to legacy-compatible versions before installing requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install pip==20.3.4 setuptools==44.1.1 wheel==0.36.2 \
  && pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace
