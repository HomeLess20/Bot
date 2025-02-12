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
    datetime.time(23,15 ): "./song/VID_20250212_225151.mp3",   #  เล่นตอน
}

VOICE_CHANNEL_ID = None  # จะเก็บ ID ห้องเสียงที่ผู้ใช้เปิดให้บอทเข้า
AUDIO_PATH = "/song"  # 🔹 เปลี่ยนเป็นที่อยู่ไฟล์จริง

# //////////////////// Bot Event /////////////////////////
@bot.event
async def on_ready():
    print(f"✅ {bot.user} has connected to Discord!")
    play_sound_at_time.start()  # เริ่ม Task ตรวจสอบเวลาเล่นเสียง

@tasks.loop(seconds=2)  # 🔹 ตรวจสอบเวลาทุก 2 วินาที
async def play_sound_at_time():
    """ตรวจสอบเวลาและเล่นเสียงตามกำหนด"""
    now = datetime.datetime.now(tz_thailand).time()

    for play_time, sound_file in play_schedule.items():
        if now.hour == play_time.hour and now.minute == play_time.minute:
            await play_audio(sound_file)
            await asyncio.sleep(60)  # ป้องกันการเล่นซ้ำใน 1 นาที

async def play_audio(audio_file):
    """เล่นไฟล์เสียงในห้องเสียง"""
    if VOICE_CHANNEL_ID:
        channel = bot.get_channel(VOICE_CHANNEL_ID)

        if channel and isinstance(channel, discord.VoiceChannel):
            try:
                # เช็คห้องเสียงที่เชื่อมต่ออยู่
                vc = channel.guild.voice_client
                if vc is not None and not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio(audio_file), after=lambda e: print(f"✅ เล่น {audio_file} เสร็จแล้ว"))
                    while vc.is_playing():
                        await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Error playing sound: {e}")
        else:
            print(f"❌ Voice Channel ID {VOICE_CHANNEL_ID} ไม่ถูกต้อง")
    else:
        print("❌ บอทยังไม่ได้เข้าห้องเสียง")

# ///////////////////// Commands /////////////////////

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}!")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# คำสั่งให้บอทเข้าห้องเสียงที่ผู้ใช้คำสั่งอยู่
@bot.command()
async def join(ctx):
    """ให้บอทเข้าห้องเสียงที่ผู้ใช้คำสั่งอยู่"""
    global VOICE_CHANNEL_ID  # ใช้ตัวแปร global เพื่ออัปเดตค่า VOICE_CHANNEL_ID
    if ctx.author.voice:
        channel = ctx.author.voice.channel  # ห้องเสียงที่ผู้ใช้กำลังอยู่
        try:
            vc = await channel.connect()
            VOICE_CHANNEL_ID = channel.id  # เก็บ ID ของห้องเสียง
            await ctx.send(f"✅ บอทเข้าห้องเสียง {channel.name} แล้ว")
        except Exception as e:
            await ctx.send(f"❌ ไม่สามารถเข้าห้องเสียงได้: {e}")
    else:
        await ctx.send("❌ คุณต้องอยู่ในห้องเสียงก่อนที่จะใช้คำสั่งนี้")

# คำสั่งให้บอทออกจากห้องเสียง
@bot.command()
async def leave(ctx):
    """ให้บอทออกจากห้องเสียง"""
    global VOICE_CHANNEL_ID  # ใช้ตัวแปร global เพื่ออัปเดตค่า VOICE_CHANNEL_ID
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        VOICE_CHANNEL_ID = None  # ตั้งค่า VOICE_CHANNEL_ID เป็น None เมื่อบอทออกจากห้องเสียง
        await ctx.send("✅ บอทออกจากห้องเสียงแล้ว")
    else:
        await ctx.send("❌ บอทไม่ได้อยู่ในห้องเสียง")

# Slash Commands
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")

# ///////////////////// Start Bot /////////////////////
server_on()  # ถ้าใช้ Replit/Heroku ให้เปิด Web Server กันหลั
bot.run(os.getenv('TOKEN'))
