# ---- base image ----
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Bangkok

# สำคัญ: libopus สำหรับ voice + ffmpeg สำหรับเล่นไฟล์เสียง
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopus0 \
    ffmpeg \
    libsodium23 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกซอร์สโค้ด
COPY . .

# รันบอท
CMD ["python", "main.py"]
