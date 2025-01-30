Python

# main.py
import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

# กำหนด intents ที่จำเป็น
intents = discord.Intents.default()
intents.message_content = True  # เปิดใช้งานถ้าบอทต้องการอ่านข้อความ
intents.members = True # เปิดใช้งานถ้าบอทต้องการเข้าถึงข้อมูลสมาชิก

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# ส่วนของการเรียกใช้งานคำสั่ง
@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

# Sync slash commands globally (once is enough, you can comment it out after the first sync)
# async def main():
#     await bot.tree.sync()

# asyncio.run(main())

server_on()
bot.run(os.getenv('TOKEN'))
