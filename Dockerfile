# ---- base image ----
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Bangkok
# ชี้ ffmpeg ให้โค้ดรู้ตำแหน่ง (main.py ใช้ตัวแปรนี้ได้)
ENV FFMPEG_PATH=/usr/bin/ffmpeg

# ----- system deps (สำคัญ: libopus) -----
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopus0 libopus-dev \
    ffmpeg \
    libsodium23 \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ----- python deps -----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ตรวจสอบว่า libopus โหลดได้จริง (ถ้าโหลดไม่ได้ให้เห็นใน log ตอน build)
RUN python - <<'PY'
import discord, sys
try:
    print("Opus pre-check (before load):", discord.opus.is_loaded())
    for name in ("libopus.so.0", "libopus-0", "libopus", "opus"):
        try:
            discord.opus.load_opus(name)
            break
        except Exception:
            pass
    print("Opus post-check (after load):", discord.opus.is_loaded())
except Exception as e:
    print("Opus check error:", e, file=sys.stderr)
PY

# ----- app code -----
COPY . .

# ----- run -----
CMD ["python", "main.py"]
