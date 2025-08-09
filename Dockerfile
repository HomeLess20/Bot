# ✅ Base image จาก Python ที่รองรับ pip และ apt
FROM python:3.11-slim

# ✅ ติดตั้ง ffmpeg
RUN apt update && apt install -y ffmpeg

# ✅ ตั้ง working directory
WORKDIR /app

# ✅ คัดลอกไฟล์ทั้งหมดไปยัง container
COPY . .

# ✅ ติดตั้ง dependency จาก requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ✅ รัน bot
CMD ["python", "main.py"]
