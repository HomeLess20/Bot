FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Bangkok
ENV FFMPEG_PATH=/usr/bin/ffmpeg

# System deps: libopus สำหรับเสียง + ffmpeg สำหรับเล่นไฟล์
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopus0 \
    ffmpeg \
    libsodium23 \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Run
CMD ["python", "main.py"]
