import os
import discord
from discord.ext import commands
import asyncio

from myserver import server_on

# กำหนด intents ที่จำเป็น
intents = discord.Intents.default()
intents.message_content = True  # เปิดใช้งานถ้าบอทต้องการอ่านข้อความ
intents.members = True  # เปิดใช้งานถ้าบอทต้องการเข้าถึงข้อมูลสมาชิก (ถ้าจำเป็น)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# ส่วนของการเรียกใช้งานคำสั่ง
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!'+str(ctx.author.name))



server_on()  # รัน web server (ถ้าจำเป็น)
token = os.getenv('TOKEN')
if token:
    bot.run(token)
else:
    print("Error: Discord bot token not found. Please set the TOKEN environment variable.")