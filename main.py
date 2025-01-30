import os
import discord
from discord.ext import commands
from discord import app_commands

from server import server_on

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())



# ส่วนของการเรียกใช้งานคำสั่ง


server_on()

bot.run(os.getenv('TOKEN'))
