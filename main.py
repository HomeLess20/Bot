import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio  # เพิ่ม import asyncio

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
@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

# Sync slash commands globally (ทำครั้งเดียว)
async def main():
    await bot.tree.sync()

asyncio.run(main())  # รัน asyncio main

server_on()  # รัน web server (ถ้าจำเป็น)
bot.run(os.getenv('TOKEN'))