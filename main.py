import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())



# ส่วนของการเรียกใช้งานคำสั่ง
@bot.event
async def on_ready():
    print("Bot is ready!")
  


server_on()

bot.run(os.getenv('TOKEN'))
