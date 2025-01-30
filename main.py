import os
import discord
import asyncio
import datetime
import pytz
from discord.ext import commands, tasks
from discord import app_commands

from myserver import server_on  # ใช้ถ้ารันบน Replit/Heroku

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# 🔹 กำหนดโซนเวลาไทย
tz_thailand = pytz.timezone("Asia/Bangkok")

# 🔹 กำหนดเวลาและไฟล์เสียง
play_schedule = {
    datetime.time(0, 8): "/song/Fe!n - Travis Scott ft.Playboi carti ｜｜ [edit audio].mp3",   #  เล่นตอน
    datetime.time(12, 0): "lunch.mp3",    # เล่นตอน 12:00 น.
    datetime.time(18, 0): "evening.mp3"   # เล่นตอน 18:00 น.
}

VOICE_CHANNEL_ID = 865206316476530708  # 🔹 ใส่ ID ของห้องเสียง
AUDIO_PATH = "/song"  # 🔹 เปลี่ยนเป็นที่อยู่ไฟล์จริง

# //////////////////// Bot Event /////////////////////////
@bot.event
async def on_ready():
    print(f"✅ {bot.user} has connected to Discord!")
    play_sound_at_time.start()  # เริ่ม Task ตรวจสอบเวลาเล่นเสียง

@tasks.loop(seconds=30)  # 🔹 ตรวจสอบเวลาทุก 30 วินาที
async def play_sound_at_time():
    """ตรวจสอบเวลาและเล่นเสียงตามกำหนด"""
    now = datetime.datetime.now(tz_thailand).time()

    for play_time, sound_file in play_schedule.items():
        if now.hour == play_time.hour and now.minute == play_time.minute:
            await play_audio(sound_file)
            await asyncio.sleep(60)  # ป้องกันการเล่นซ้ำใน 1 นาที

async def play_audio(audio_file):
    """เข้าห้องเสียงและเล่นไฟล์"""
    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(audio_file), after=lambda e: print(f"✅ เล่น {audio_file} เสร็จแล้ว"))
            while vc.is_playing():
                await asyncio.sleep(1)
            await vc.disconnect()
        except Exception as e:
            print(f"❌ Error playing sound: {e}")
    else:
        print(f"❌ Voice Channel ID {VOICE_CHANNEL_ID} ไม่ถูกต้อง")

# ///////////////////// Commands /////////////////////
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}!")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# Slash Commands
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")

# ///////////////////// Start Bot /////////////////////
server_on()  # ถ้าใช้ Replit/Heroku ให้เปิด Web Server กันหลับ
bot.run(os.getenv('TOKEN'))
