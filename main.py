import os
import asyncio
import datetime
import pytz
import discord
from discord.ext import commands, tasks
from discord import app_commands

from myserver import server_on  # ใช้ถ้ารันบน Railway/Render/Replit เพื่อกัน sleep

# -------------------- Intents & Bot --------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True  # สำคัญสำหรับ voice

bot = commands.Bot(command_prefix='!', intents=intents)

# -------------------- Opus & FFmpeg helpers --------------------
def ensure_opus_loaded():
    """
    พยายามโหลด Opus ถ้ายังไม่ถูกโหลด (Windows/Linux)
    ถ้าติดตั้ง libopus/opus.dll ถูกต้อง จะขึ้น True
    """
    if discord.opus.is_loaded():
        return True
    candidates = ["libopus-0", "libopus", "opus"]
    for name in candidates:
        try:
            discord.opus.load_opus(name)
            break
        except Exception:
            continue
    print("Opus loaded:", discord.opus.is_loaded())
    if not discord.opus.is_loaded():
        print("⚠️  Opus ยังไม่ถูกโหลด ตรวจสอบการติดตั้ง libopus/opus.dll")
    return discord.opus.is_loaded()

def ffmpeg_source(path: str) -> discord.AudioSource:
    """
    คืน FFmpegPCMAudio โดยใช้ตัวแปรแวดล้อม FFMPEG_PATH หากตั้งไว้
    """
    ffmpeg_bin = os.environ.get("FFMPEG_PATH", "ffmpeg")
    return discord.FFmpegPCMAudio(path, executable=ffmpeg_bin)

# -------------------- Config --------------------
tz_thailand = pytz.timezone("Asia/Bangkok")

# ห้องเสียงที่ให้บอทเล่นเสียง (จะอัปเดตตอนใช้ !join)
VOICE_CHANNEL_ID = None

# โฟลเดอร์เพลง (ไม่บังคับใช้ แต่เผื่อย้ายที่เก็บในอนาคต)
AUDIO_DIR = "./song"

# -------------------- ตารางเวลา --------------------
play_schedule = {
    # หวยลาว Extra
    datetime.time(8, 14): "./song/หวยลาว Extra 10 นาที.MP3",
    datetime.time(8, 19): "./song/หวยลาว Extra 5 นาที.MP3",
    datetime.time(8, 21): "./song/หวยลาว Extra 3 นาที.MP3",

    # นิเคอิ(เช้า) VIP
    datetime.time(8, 49): "./song/นิเคอิ(เช้า) VIP 10 นาที.MP3",
    datetime.time(8, 54): "./song/นิเคอิ(เช้า) VIP 5 นาที.MP3",
    datetime.time(8, 56): "./song/นิเคอิ(เช้า) VIP 3 นาที.MP3",

    # ฮานอยอาเซียน
    datetime.time(8, 59): "./song/ฮานอยอาเซียน 10 นาที.MP3",
    datetime.time(9, 4): "./song/ฮานอยอาเซียน 5 นาที.MP3",
    datetime.time(9, 6): "./song/ฮานอยอาเซียน 3 นาที.MP3",

    # นิเคอิ รอบเช้า
    datetime.time(9, 11): "./song/นิเคอิ รอบเช้า 10 นาที.MP3",
    datetime.time(9, 16): "./song/นิเคอิ รอบเช้า 5 นาที.MP3",
    datetime.time(9, 18): "./song/นิเคอิ รอบเช้า 3 นาที.MP3",

    # จีน(เช้า) VIP
    datetime.time(9, 49): "./song/จีน(เช้า) VIP 10 นาที.MP3",
    datetime.time(9, 54): "./song/จีน(เช้า) VIP 5 นาที.MP3",
    datetime.time(9, 56): "./song/จีน(เช้า) VIP 3 นาที.MP3",

    # จีนรอบเช้า
    datetime.time(10, 9): "./song/จีนรอบเช้า 10 นาที.MP3",
    datetime.time(10, 14): "./song/จีนรอบเช้า 5 นาที.MP3",
    datetime.time(10, 16): "./song/จีนรอบเช้า 3 นาที.MP3",

    # หวยลาว TV
    datetime.time(10, 14, 8): "./song/หวยลาว TV 10 นาที.MP3",
    datetime.time(10, 19): "./song/หวยลาว TV 5 นาที.MP3",
    datetime.time(10, 21): "./song/หวยลาว TV 3 นาที.MP3",

    # ฮั่งเส็ง(เช้า) VIP
    datetime.time(10, 19, 8): "./song/ฮั่งเส็ง(เช้า) VIP 10 นาที.MP3",
    datetime.time(10, 24): "./song/ฮั่งเส็ง(เช้า) VIP 5 นาที.MP3",
    datetime.time(10, 26): "./song/ฮั่งเส็ง(เช้า) VIP 3 นาที.MP3",

    # ฮั่งเส็งรอบเช้า
    datetime.time(10, 41): "./song/ฮั่งเส็งรอบเช้า 10 นาที.MP3",
    datetime.time(10, 46): "./song/ฮั่งเส็งรอบเช้า 5 นาที.MP3",
    datetime.time(10, 48): "./song/ฮั่งเส็งรอบเช้า 3 นาที.MP3",

    # ฮานอย HD
    datetime.time(10, 59): "./song/ฮานอย HD 10 นาที.MP3",
    datetime.time(11, 4): "./song/ฮานอย HD 5 นาที.MP3",
    datetime.time(11, 6): "./song/ฮานอย HD 3 นาที.MP3",

    # ไต้หวัน VIP
    datetime.time(11, 19): "./song/ไต้หวัน VIP 10 นาที.MP3",
    datetime.time(11, 24): "./song/ไต้หวัน VIP 5 นาที.MP3",
    datetime.time(11, 26): "./song/ไต้หวัน VIP 3 นาที.MP3",

    # หุ้นไทยพิเศษเที่ยง
    datetime.time(11, 34): "./song/หุ้นไทยพิเศษเที่ยง 10 นาที.MP3",
    datetime.time(11, 39): "./song/หุ้นไทยพิเศษเที่ยง 5 นาที.MP3",
    datetime.time(11, 41): "./song/หุ้นไทยพิเศษเที่ยง 3 นาที.MP3",

    # ฮานอย สตาร์
    datetime.time(11, 59): "./song/ฮานอย สตาร์ 10 นาที.MP3",
    datetime.time(12, 4): "./song/ฮานอย สตาร์ 5 นาที.MP3",
    datetime.time(12, 6): "./song/ฮานอย สตาร์ 3 นาที.MP3",

    # หุ้นไต้หวัน
    datetime.time(11, 59, 8): "./song/หุ้นไต้หวัน 10 นาที.MP3",
    datetime.time(12, 4, 8): "./song/หุ้นไต้หวัน 5 นาที.MP3",
    datetime.time(12, 6, 8): "./song/หุ้นไต้หวัน 3 นาที.MP3",

    # เกาหลี VIP
    datetime.time(12, 19): "./song/เกาหลี VIP 10 นาที.MP3",
    datetime.time(12, 24): "./song/เกาหลี VIP 5 นาที.MP3",
    datetime.time(12, 26): "./song/เกาหลี VIP 3 นาที.MP3",

    # หุ้นเกาหลี
    datetime.time(12, 34): "./song/หุ้นเกาหลี 10 นาที.MP3",
    datetime.time(12, 39): "./song/หุ้นเกาหลี 5 นาที.MP3",
    datetime.time(12, 41): "./song/หุ้นเกาหลี 3 นาที.MP3",

    # นิเคอิ รอบบ่าย
    datetime.time(12, 41, 8): "./song/นิเคอิ รอบบ่าย 10 นาที.MP3",
    datetime.time(12, 46): "./song/นิเคอิ รอบบ่าย 5 นาที.MP3",
    datetime.time(12, 48): "./song/นิเคอิ รอบบ่าย 3 นาที.MP3",

    # นิเคอิ(บ่าย) VIP
    datetime.time(13, 9): "./song/นิเคอิ(บ่าย) VIP 10 นาที.MP3",
    datetime.time(13, 14): "./song/นิเคอิ(บ่าย) VIP 5 นาที.MP3",
    datetime.time(13, 16): "./song/นิเคอิ(บ่าย) VIP 3 นาที.MP3",

    # หวยลาว HD
    datetime.time(13, 29): "./song/หวยลาว HD 10 นาที.MP3",
    datetime.time(13, 34): "./song/หวยลาว HD 5 นาที.MP3",
    datetime.time(13, 36): "./song/หวยลาว HD 3 นาที.MP3",

    # จีนรอบบ่าย
    datetime.time(13, 34, 8): "./song/จีนรอบบ่าย 10 นาที.MP3",
    datetime.time(13, 39): "./song/จีนรอบบ่าย 5 นาที.MP3",
    datetime.time(13, 41): "./song/จีนรอบบ่าย 3 นาที.MP3",

    # หวยฮานอย TV
    datetime.time(13, 59): "./song/หวยฮานอย TV 10 นาที.MP3",
    datetime.time(14, 4): "./song/หวยฮานอย TV 5 นาที.MP3",
    datetime.time(14, 6): "./song/หวยฮานอย TV 3 นาที.MP3",

    # จีน(บ่าย) VIP
    datetime.time(14, 9): "./song/จีน(บ่าย) VIP 10 นาที.MP3",
    datetime.time(14, 14): "./song/จีน(บ่าย) VIP 5 นาที.MP3",
    datetime.time(14, 16): "./song/จีน(บ่าย) VIP 3 นาที.MP3",

    # ฮั่งเส็งรอบบ่าย
    datetime.time(14, 41): "./song/ฮั่งเส็งรอบบ่าย 10 นาที.MP3",
    datetime.time(14, 46): "./song/ฮั่งเส็งรอบบ่าย 5 นาที.MP3",
    datetime.time(14, 48): "./song/ฮั่งเส็งรอบบ่าย 3 นาที.MP3",

    # ฮั่งเส็ง(บ่าย) VIP
    datetime.time(15, 9): "./song/ฮั่งเส็ง(บ่าย) VIP 10 นาที.MP3",
    datetime.time(15, 14): "./song/ฮั่งเส็ง(บ่าย) VIP 5 นาที.MP3",
    datetime.time(15, 16): "./song/ฮั่งเส็ง(บ่าย) VIP 3 นาที.MP3",

    # หวยลาว สตาร์
    datetime.time(15, 29): "./song/หวยลาว สตาร์ 10 นาที.MP3",
    datetime.time(15, 34): "./song/หวยลาว สตาร์ 5 นาที.MP3",
    datetime.time(15, 36): "./song/หวยลาว สตาร์ 3 นาที.MP3",

    # หุ้นไทยพิเศษบ่าย
    datetime.time(15, 34, 8): "./song/หุ้นไทยพิเศษบ่าย 10 นาที.MP3",
    datetime.time(15, 39): "./song/หุ้นไทยพิเศษบ่าย 5 นาที.MP3",
    datetime.time(15, 41): "./song/หุ้นไทยพิเศษบ่าย 3 นาที.MP3",

    # หุ้นสิงคโปร์
    datetime.time(15, 44): "./song/หุ้นสิงคโปร์ 10 นาที.MP3",
    datetime.time(15, 49): "./song/หุ้นสิงคโปร์ 5 นาที.MP3",
    datetime.time(15, 51): "./song/หุ้นสิงคโปร์ 3 นาที.MP3",

    # หุ้นไทยปิดเย็น
    datetime.time(15, 54): "./song/หุ้นไทยปิดเย็น 10 นาที.MP3",
    datetime.time(15, 59): "./song/หุ้นไทยปิดเย็น 5 นาที.MP3",
    datetime.time(16, 1): "./song/หุ้นไทยปิดเย็น 3 นาที.MP3",

    # หวยฮานอย กาชาด
    datetime.time(15, 59, 8): "./song/หวยฮานอย กาชาด 10 นาที.MP3",
    datetime.time(16, 4): "./song/หวยฮานอย กาชาด 5 นาที.MP3",
    datetime.time(16, 6): "./song/หวยฮานอย กาชาด 3 นาที.MP3",

    # หุ้นอินเดีย
    datetime.time(16, 39): "./song/หุ้นอินเดีย 10 นาที.MP3",
    datetime.time(16, 44): "./song/หุ้นอินเดีย 5 นาที.MP3",
    datetime.time(16, 46): "./song/หุ้นอินเดีย 3 นาที.MP3",

    # สิงคโปร์ VIP
    datetime.time(16, 49): "./song/สิงคโปร์ VIP 10 นาที.MP3",
    datetime.time(16, 54): "./song/สิงคโปร์ VIP 5 นาที.MP3",
    datetime.time(16, 56): "./song/สิงคโปร์ VIP 3 นาที.MP3",

    # ฮานอยสามัคคี
    datetime.time(16, 59): "./song/ฮานอยสามัคคี 10 นาที.MP3",
    datetime.time(17, 4): "./song/ฮานอยสามัคคี 5 นาที.MP3",
    datetime.time(17, 6): "./song/ฮานอยสามัคคี 3 นาที.MP3",

    # ฮานอยพิเศษ
    datetime.time(17, 1): "./song/ฮานอยพิเศษ 10 นาที.MP3",
    datetime.time(17, 6, 8): "./song/ฮานอยพิเศษ 5 นาที.MP3",
    datetime.time(17, 8): "./song/ฮานอยพิเศษ 3 นาที.MP3",

    # หวยฮานอย
    datetime.time(18, 1): "./song/หวยฮานอย 10 นาที.MP3",
    datetime.time(18, 6): "./song/หวยฮานอย 5 นาที.MP3",
    datetime.time(18, 8): "./song/หวยฮานอย 3 นาที.MP3",

    # หวยฮานอย VIP # ฮานอยพัฒนา
    datetime.time(18, 59): "./song/หวยฮานอย VIP 10 นาที.MP3",
    datetime.time(19, 4): "./song/หวยฮานอย VIP 5 นาที.MP3",
    datetime.time(19, 6): "./song/หวยฮานอย VIP 3 นาที.MP3",

    # หวยลาว
    datetime.time(20, 7): "./song/หวยลาว 10 นาที.MP3",
    datetime.time(20, 12): "./song/หวยลาว 5 นาที.MP3",
    datetime.time(20, 14): "./song/หวยลาว 3 นาที.MP3",

    # หวยลาวสามัคคี
    datetime.time(20, 9): "./song/หวยลาวสามัคคี 10 นาที.MP3",
    datetime.time(20, 14, 8): "./song/หวยลาวสามัคคี 5 นาที.MP3",
    datetime.time(20, 16): "./song/หวยลาวสามัคคี 3 นาที.MP3",

    # ลาวอาเซียน
    datetime.time(20, 44): "./song/ลาวอาเซียน 10 นาที.MP3",
    datetime.time(20, 49): "./song/ลาวอาเซียน 5 นาที.MP3",
    datetime.time(20, 51): "./song/ลาวอาเซียน 3 นาที.MP3",

    # หวยลาว VIP
    datetime.time(21, 9): "./song/หวยลาว VIP 10 นาที.MP3",
    datetime.time(21, 14): "./song/หวยลาว VIP 5 นาที.MP3",
    datetime.time(21, 16): "./song/หวยลาว VIP 3 นาที.MP3",

    # หวยลาวสามัคคี VIP
    datetime.time(21, 14, 8): "./song/หวยลาวสามัคคี VIP 10 นาที.MP3",
    datetime.time(21, 19): "./song/หวยลาวสามัคคี VIP 5 นาที.MP3",
    datetime.time(21, 21): "./song/หวยลาวสามัคคี VIP 3 นาที.MP3",

    # หวยลาว STAR VIP # อังกฤษ VIP
    datetime.time(21, 34): "./song/หวยลาว STAR VIP 10 นาที.MP3",
    datetime.time(21, 39): "./song/หวยลาว STAR VIP 5 นาที.MP3",
    datetime.time(21, 41): "./song/หวยลาว STAR VIP 3 นาที.MP3",

    # หวยฮานอย Extra
    datetime.time(21, 59): "./song/หวยฮานอย Extra 10 นาที.MP3",
    datetime.time(22, 4): "./song/หวยฮานอย Extra 5 นาที.MP3",
    datetime.time(22, 6): "./song/หวยฮานอย Extra 3 นาที.MP3",

    # หุ้นอังกฤษ
    datetime.time(22, 4, 8): "./song/หุ้นอังกฤษ 10 นาที.MP3",
    datetime.time(22, 9): "./song/หุ้นอังกฤษ 5 นาที.MP3",
    datetime.time(22, 11): "./song/หุ้นอังกฤษ 3 นาที.MP3",

    # หุ้นเยอรมัน
    datetime.time(22, 4, 16): "./song/หุ้นเยอรมัน 10 นาที.MP3",
    datetime.time(22, 9, 8): "./song/หุ้นเยอรมัน 5 นาที.MP3",
    datetime.time(22, 11, 8): "./song/หุ้นเยอรมัน 3 นาที.MP3",

    # หุ้นรัสเซีย
    datetime.time(22, 19): "./song/หุ้นรัสเซีย 10 นาที.MP3",
    datetime.time(22, 24): "./song/หุ้นรัสเซีย 5 นาที.MP3",
    datetime.time(22, 26): "./song/หุ้นรัสเซีย 3 นาที.MP3",

    # เยอรมัน VIP
    datetime.time(22, 34): "./song/เยอรมัน VIP 10 นาที.MP3",
    datetime.time(22, 39): "./song/เยอรมัน VIP 5 นาที.MP3",
    datetime.time(22, 41): "./song/เยอรมัน VIP 3 นาที.MP3",

    # หวยลาว กาชาด
    datetime.time(23, 14): "./song/หวยลาว กาชาด 10 นาที.MP3",
    datetime.time(23, 19): "./song/หวยลาว กาชาด 5 นาที.MP3",
    datetime.time(23, 21): "./song/หวยลาว กาชาด 3 นาที.MP3",

    # รัสเซีย VIP
    datetime.time(23, 34): "./song/รัสเซีย VIP 10 นาที.MP3",
    datetime.time(23, 39): "./song/รัสเซีย VIP 5 นาที.MP3",
    datetime.time(23, 41): "./song/รัสเซีย VIP 3 นาที.MP3",

    # หวยดาวโจนส์ VIP
    datetime.time(23, 59): "./song/หวยดาวโจนส์ VIP 10 นาที.MP3",
    datetime.time(0, 4): "./song/หวยดาวโจนส์ VIP 5 นาที.MP3",
    datetime.time(0, 6): "./song/หวยดาวโจนส์ VIP 3 นาที.MP3",

    # หวยดาวโจนส์ STAR
    datetime.time(0, 54): "./song/หวยดาวโจนส์ STAR 10 นาที.MP3",
    datetime.time(0, 59, 8): "./song/หวยดาวโจนส์ STAR 5 นาที.MP3",
    datetime.time(1, 1): "./song/หวยดาวโจนส์ STAR 3 นาที.MP3",
}

# -------------------- Events & Tasks --------------------
@bot.event
async def on_ready():
    print(f"✅ {bot.user} has connected to Discord!")
    ensure_opus_loaded()
    try:
        await bot.tree.sync()
    except Exception as e:
        print("Slash sync error:", e)
    play_sound_at_time.start()

@tasks.loop(seconds=2)
async def play_sound_at_time():
    """ตรวจสอบเวลาและเล่นเสียงตามกำหนด (เทียบชั่วโมง/นาที)"""
    now = datetime.datetime.now(tz_thailand).time()
    for play_time, sound_file in play_schedule.items():
        if now.hour == play_time.hour and now.minute == play_time.minute:
            await play_audio(sound_file)
            await asyncio.sleep(60)  # กันเล่นซ้ำในนาทีเดียวกัน

async def play_audio(audio_file: str):
    """เล่นไฟล์เสียงในห้องเสียง (auto-join ถ้ายังไม่ต่อ)"""
    global VOICE_CHANNEL_ID
    if not VOICE_CHANNEL_ID:
        print("❌ ยังไม่ได้ตั้ง VOICE_CHANNEL_ID (ให้ใช้คำสั่ง !join ก่อน)")
        return

    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.VoiceChannel):
        print(f"❌ Voice Channel ID {VOICE_CHANNEL_ID} ไม่ถูกต้อง")
        return

    try:
        vc = channel.guild.voice_client
        if vc is None or not vc.is_connected():
            vc = await channel.connect()
            await asyncio.sleep(1)

        if not vc.is_playing():
            print(f"▶️ Playing: {audio_file}")
            src = ffmpeg_source(audio_file)
            vc.play(src, after=lambda e: print(f"✅ เล่นเสร็จ: {audio_file} | err={e}"))
            while vc.is_playing():
                await asyncio.sleep(1)
        else:
            print("ℹ️ กำลังเล่นเสียงอยู่ ข้ามไฟล์นี้")
    except Exception as e:
        print(f"❌ Error playing sound: {e}")

# -------------------- Text Commands --------------------
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}!")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def join(ctx):
    """ให้บอทเข้าห้องเสียงที่ผู้ใช้คำสั่งอยู่ และตั้ง VOICE_CHANNEL_ID"""
    global VOICE_CHANNEL_ID
    if not ctx.author.voice:
        await ctx.send("❌ คุณต้องอยู่ในห้องเสียงก่อนที่จะใช้คำสั่งนี้")
        return

    channel = ctx.author.voice.channel
    try:
        if ctx.voice_client and ctx.voice_client.channel.id == channel.id:
            await ctx.send(f"ℹ️ บอทอยู่ใน {channel.name} อยู่แล้ว")
        else:
            await channel.connect()
            await asyncio.sleep(1)
        VOICE_CHANNEL_ID = channel.id
        await ctx.send(f"✅ บอทเข้าห้องเสียง {channel.name} แล้ว (ID: {VOICE_CHANNEL_ID})")
    except Exception as e:
        await ctx.send(f"❌ ไม่สามารถเข้าห้องเสียงได้: {e}")

@bot.command()
async def leave(ctx):
    """ให้บอทออกจากห้องเสียง และล้าง VOICE_CHANNEL_ID"""
    global VOICE_CHANNEL_ID
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
        VOICE_CHANNEL_ID = None
        await ctx.send("✅ บอทออกจากห้องเสียงแล้ว")
    else:
        await ctx.send("❌ บอทไม่ได้อยู่ในห้องเสียง")

# -------------------- Slash Commands --------------------
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")

# -------------------- Start --------------------
server_on()  # เปิดเว็บกัน sleep (ถ้าโฮสต์ต้องการ)
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise RuntimeError("ไม่พบ TOKEN ใน environment variables")
bot.run(TOKEN)
