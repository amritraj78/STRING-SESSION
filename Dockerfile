FROM python:3.10-slim

WORKDIR /app

# Install system build dependencies and git
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && (find /usr/local/lib/python*/site-packages/pyrogram1/ -type f -name "*.py" -exec sed -i 's/from pyrogram import raw/from pyrogram1 import raw/g' {} + || true)

# Copy source code
COPY . .

# Default port for Koyeb web service health checks
ENV PORT=8000
EXPOSE 8000

CMD ["python3", "main.py"]
