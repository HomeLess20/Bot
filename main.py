import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from myserver import server_on  # ถ้าจำเป็นต้องใช้

# กำหนด intents ที่จำเป็น
intents = discord.Intents.default()
intents.message_content = True  # ถ้าบอทต้องการอ่านข้อความ
intents.members = True  # ถ้าบอทต้องการเข้าถึงข้อมูลสมาชิก (ถ้าจำเป็น)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Slash command ที่ตอบ Hi User
@bot.tree.command(name="hello", description="Say hi to the user!")
async def hello(interaction: discord.Interaction):
    user = interaction.user  # ดึงข้อมูลผู้ใช้ที่เรียกคำสั่ง
    await interaction.response.send_message(f"Hi {user.mention}!")  # ตอบกลับพร้อม mention ผู้ใช้

# หรือถ้าต้องการให้บอทตอบกลับเป็นข้อความธรรมดา (ไม่ mention)
# @bot.tree.command(name="hello", description="Say hi to the user!")
# async def hello(interaction: discord.Interaction):
#     user = interaction.user
#     await interaction.response.send_message(f"Hi {user.name}!")

@bot.event
async def on_message(message):
    # ตรวจสอบว่าข้อความนั้นมาจากบอทเองหรือไม่ ถ้าใช่ ไม่ต้องทำอะไร
    if message.author == bot.user:
        return

    mes = message.content  # ดึงข้อความที่ผู้ใช้ส่งมา

    if mes == 'hello':
        await message.channel.send("Hello It's me")  # ส่งข้อความตอบกลับไปที่แชนแนลเดิม


# Sync slash commands globally (ทำครั้งเดียว)
async def main():
    await bot.tree.sync()

asyncio.run(main())  # รัน asyncio main

server_on()  # รัน web server (ถ้าจำเป็น)
bot.run(os.getenv('TOKEN'))