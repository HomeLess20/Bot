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
   
# หวยลาว Extra
datetime.time(8, 15): "./song/หวยลาว Extra 10 นาที.MP3",  # หวยลาว Extra ก่อนปิด 10 นาที: 08:15
datetime.time(8, 20): "./song/หวยลาว Extra 5 นาที.MP3",  # หวยลาว Extra ก่อนปิด 5 นาที: 08:20
datetime.time(8, 22): "./song/หวยลาว Extra 3 นาที.MP3",  # หวยลาว Extra ก่อนปิด 3 นาที: 08:22

# นิเคอิ(เช้า) VIP
datetime.time(8, 50): "./song/นิเคอิ(เช้า) VIP 10 นาที.MP3",  # นิเคอิ(เช้า) VIP ก่อนปิด 10 นาที: 08:50
datetime.time(8, 55): "./song/นิเคอิ(เช้า) VIP 5 นาที.MP3",  # นิเคอิ(เช้า) VIP ก่อนปิด 5 นาที: 08:55
datetime.time(8, 57): "./song/นิเคอิ(เช้า) VIP 3 นาที.MP3",  # นิเคอิ(เช้า) VIP ก่อนปิด 3 นาที: 08:57

# ฮานอยอาเซียน
datetime.time(9, 0): "./song/ฮานอยอาเซียน 10 นาที.MP3",  # ฮานอยอาเซียน ก่อนปิด 10 นาที: 09:00
datetime.time(9, 5): "./song/ฮานอยอาเซียน 5 นาที.MP3",  # ฮานอยอาเซียน ก่อนปิด 5 นาที: 09:05
datetime.time(9, 7): "./song/ฮานอยอาเซียน 3 นาที.MP3",  # ฮานอยอาเซียน ก่อนปิด 3 นาที: 09:07

# นิเคอิ รอบเช้า
datetime.time(9, 12): "./song/นิเคอิ รอบเช้า 10 นาที.MP3",  # นิเคอิ รอบเช้า ก่อนปิด 10 นาที: 09:12
datetime.time(9, 17): "./song/นิเคอิ รอบเช้า 5 นาที.MP3",  # นิเคอิ รอบเช้า ก่อนปิด 5 นาที: 09:17
datetime.time(9, 19): "./song/นิเคอิ รอบเช้า 3 นาที.MP3",  # นิเคอิ รอบเช้า ก่อนปิด 3 นาที: 09:19

# จีน(เช้า) VIP
datetime.time(9, 50): "./song/จีน(เช้า) VIP 10 นาที.MP3",  # จีน(เช้า) VIP ก่อนปิด 10 นาที: 09:50
datetime.time(9, 55): "./song/จีน(เช้า) VIP 5 นาที.MP3",  # จีน(เช้า) VIP ก่อนปิด 5 นาที: 09:55
datetime.time(9, 57): "./song/จีน(เช้า) VIP 3 นาที.MP3",  # จีน(เช้า) VIP ก่อนปิด 3 นาที: 09:57

# จีนรอบเช้า
datetime.time(10, 10): "./song/จีนรอบเช้า 10 นาที.MP3",  # จีนรอบเช้า ก่อนปิด 10 นาที: 10:10
datetime.time(10, 15): "./song/จีนรอบเช้า 5 นาที.MP3",  # จีนรอบเช้า ก่อนปิด 5 นาที: 10:15
datetime.time(10, 17): "./song/จีนรอบเช้า 3 นาที.MP3",  # จีนรอบเช้า ก่อนปิด 3 นาที: 10:17

# หวยลาว TV
datetime.time(10, 15): "./song/หวยลาว TV 10 นาที.MP3",  # หวยลาว TV ก่อนปิด 10 นาที: 10:15
datetime.time(10, 20): "./song/หวยลาว TV 5 นาที.MP3",  # หวยลาว TV ก่อนปิด 5 นาที: 10:20
datetime.time(10, 22): "./song/หวยลาว TV 3 นาที.MP3",  # หวยลาว TV ก่อนปิด 3 นาที: 10:22

# ฮั่งเส็ง(เช้า) VIP
datetime.time(10, 20): "./song/ฮั่งเส็ง(เช้า) VIP 10 นาที.MP3",  # ฮั่งเส็ง(เช้า) VIP ก่อนปิด 10 นาที: 10:20
datetime.time(10, 25): "./song/ฮั่งเส็ง(เช้า) VIP 5 นาที.MP3",  # ฮั่งเส็ง(เช้า) VIP ก่อนปิด 5 นาที: 10:25
datetime.time(10, 27): "./song/ฮั่งเส็ง(เช้า) VIP 3 นาที.MP3",  # ฮั่งเส็ง(เช้า) VIP ก่อนปิด 3 นาที: 10:27

# ฮั่งเส็งรอบเช้า
datetime.time(10, 42): "./song/ฮั่งเส็งรอบเช้า 10 นาที.MP3",  # ฮั่งเส็งรอบเช้า ก่อนปิด 10 นาที: 10:42
datetime.time(10, 47): "./song/ฮั่งเส็งรอบเช้า 5 นาที.MP3",  # ฮั่งเส็งรอบเช้า ก่อนปิด 5 นาที: 10:47
datetime.time(10, 49): "./song/ฮั่งเส็งรอบเช้า 3 นาที.MP3",  # ฮั่งเส็งรอบเช้า ก่อนปิด 3 นาที: 10:49

# ฮานอย HD
datetime.time(11, 0): "./song/ฮานอย HD 10 นาที.MP3",  # ฮานอย HD ก่อนปิด 10 นาที: 11:00
datetime.time(11, 5): "./song/ฮานอย HD 5 นาที.MP3",  # ฮานอย HD ก่อนปิด 5 นาที: 11:05
datetime.time(11, 7): "./song/ฮานอย HD 3 นาที.MP3",  # ฮานอย HD ก่อนปิด 3 นาที: 11:07

# ไต้หวัน VIP
datetime.time(11, 20): "./song/ไต้หวัน VIP 10 นาที.MP3",  # ไต้หวัน VIP ก่อนปิด 10 นาที: 11:20
datetime.time(11, 25): "./song/ไต้หวัน VIP 5 นาที.MP3",  # ไต้หวัน VIP ก่อนปิด 5 นาที: 11:25
datetime.time(11, 27): "./song/ไต้หวัน VIP 3 นาที.MP3",  # ไต้หวัน VIP ก่อนปิด 3 นาที: 11:27

# หุ้นไทยพิเศษเที่ยง
datetime.time(11, 35): "./song/หุ้นไทยพิเศษเที่ยง 10 นาที.MP3",  # หุ้นไทยพิเศษเที่ยง ก่อนปิด 10 นาที: 11:35
datetime.time(11, 40): "./song/หุ้นไทยพิเศษเที่ยง 5 นาที.MP3",  # หุ้นไทยพิเศษเที่ยง ก่อนปิด 5 นาที: 11:40
datetime.time(11, 42): "./song/หุ้นไทยพิเศษเที่ยง 3 นาที.MP3",  # หุ้นไทยพิเศษเที่ยง ก่อนปิด 3 นาที: 11:42

# ฮานอย สตาร์
datetime.time(12, 0): "./song/ฮานอย สตาร์ 10 นาที.MP3",  # ฮานอย สตาร์ ก่อนปิด 10 นาที: 12:00
datetime.time(12, 5): "./song/ฮานอย สตาร์ 5 นาที.MP3",  # ฮานอย สตาร์ ก่อนปิด 5 นาที: 12:05
datetime.time(12, 7): "./song/ฮานอย สตาร์ 3 นาที.MP3",  # ฮานอย สตาร์ ก่อนปิด 3 นาที: 12:07

# หุ้นไต้หวัน
datetime.time(12, 0): "./song/หุ้นไต้หวัน 10 นาที.MP3",  # หุ้นไต้หวัน ก่อนปิด 10 นาที: 12:00
datetime.time(12, 5): "./song/หุ้นไต้หวัน 5 นาที.MP3",  # หุ้นไต้หวัน ก่อนปิด 5 นาที: 12:05
datetime.time(12, 7): "./song/หุ้นไต้หวัน 3 นาที.MP3",  # หุ้นไต้หวัน ก่อนปิด 3 นาที: 12:07

# เกาหลี VIP
datetime.time(12, 20): "./song/เกาหลี VIP 10 นาที.MP3",  # เกาหลี VIP ก่อนปิด 10 นาที: 12:20
datetime.time(12, 25): "./song/เกาหลี VIP 5 นาที.MP3",  # เกาหลี VIP ก่อนปิด 5 นาที: 12:25
datetime.time(12, 27): "./song/เกาหลี VIP 3 นาที.MP3",  # เกาหลี VIP ก่อนปิด 3 นาที: 12:27

# หุ้นเกาหลี
datetime.time(12, 35): "./song/หุ้นเกาหลี 10 นาที.MP3",  # หุ้นเกาหลี ก่อนปิด 10 นาที: 12:35
datetime.time(12, 40): "./song/หุ้นเกาหลี 5 นาที.MP3",  # หุ้นเกาหลี ก่อนปิด 5 นาที: 12:40
datetime.time(12, 42): "./song/หุ้นเกาหลี 3 นาที.MP3",  # หุ้นเกาหลี ก่อนปิด 3 นาที: 12:42

# นิเคอิ รอบบ่าย
datetime.time(12, 42): "./song/นิเคอิ รอบบ่าย 10 นาที.MP3",  # นิเคอิ รอบบ่าย ก่อนปิด 10 นาที: 12:42
datetime.time(12, 47): "./song/นิเคอิ รอบบ่าย 5 นาที.MP3",  # นิเคอิ รอบบ่าย ก่อนปิด 5 นาที: 12:47
datetime.time(12, 49): "./song/นิเคอิ รอบบ่าย 3 นาที.MP3",  # นิเคอิ รอบบ่าย ก่อนปิด 3 นาที: 12:49

# นิเคอิ(บ่าย) VIP
datetime.time(13, 10): "./song/นิเคอิ(บ่าย) VIP 10 นาที.MP3",  # นิเคอิ(บ่าย) VIP ก่อนปิด 10 นาที: 13:10
datetime.time(13, 15): "./song/นิเคอิ(บ่าย) VIP 5 นาที.MP3",  # นิเคอิ(บ่าย) VIP ก่อนปิด 5 นาที: 13:15
datetime.time(13, 17): "./song/นิเคอิ(บ่าย) VIP 3 นาที.MP3",  # นิเคอิ(บ่าย) VIP ก่อนปิด 3 นาที: 13:17

# หวยลาว HD
datetime.time(13, 30): "./song/หวยลาว HD 10 นาที.MP3",  # หวยลาว HD ก่อนปิด 10 นาที: 13:30
datetime.time(13, 35): "./song/หวยลาว HD 5 นาที.MP3",  # หวยลาว HD ก่อนปิด 5 นาที: 13:35
datetime.time(13, 37): "./song/หวยลาว HD 3 นาที.MP3",  # หวยลาว HD ก่อนปิด 3 นาที: 13:37

# จีนรอบบ่าย
datetime.time(13, 35): "./song/จีนรอบบ่าย 10 นาที.MP3",  # จีนรอบบ่าย ก่อนปิด 10 นาที: 13:35
datetime.time(13, 40): "./song/จีนรอบบ่าย 5 นาที.MP3",  # จีนรอบบ่าย ก่อนปิด 5 นาที: 13:40
datetime.time(13, 42): "./song/จีนรอบบ่าย 3 นาที.MP3",  # จีนรอบบ่าย ก่อนปิด 3 นาที: 13:42

# หวยฮานอย TV
datetime.time(14, 0): "./song/หวยฮานอย TV 10 นาที.MP3",  # หวยฮานอย TV ก่อนปิด 10 นาที: 14:00
datetime.time(14, 5): "./song/หวยฮานอย TV 5 นาที.MP3",  # หวยฮานอย TV ก่อนปิด 5 นาที: 14:05
datetime.time(14, 7): "./song/หวยฮานอย TV 3 นาที.MP3",  # หวยฮานอย TV ก่อนปิด 3 นาที: 14:07

# จีน(บ่าย) VIP
datetime.time(14, 10): "./song/จีน(บ่าย) VIP 10 นาที.MP3",  # จีน(บ่าย) VIP ก่อนปิด 10 นาที: 14:10
datetime.time(14, 15): "./song/จีน(บ่าย) VIP 5 นาที.MP3",  # จีน(บ่าย) VIP ก่อนปิด 5 นาที: 14:15
datetime.time(14, 17): "./song/จีน(บ่าย) VIP 3 นาที.MP3",  # จีน(บ่าย) VIP ก่อนปิด 3 นาที: 14:17

# ฮั่งเส็งรอบบ่าย
datetime.time(14, 42): "./song/ฮั่งเส็งรอบบ่าย 10 นาที.MP3",  # ฮั่งเส็งรอบบ่าย ก่อนปิด 10 นาที: 14:42
datetime.time(14, 47): "./song/ฮั่งเส็งรอบบ่าย 5 นาที.MP3",  # ฮั่งเส็งรอบบ่าย ก่อนปิด 5 นาที: 14:47
datetime.time(14, 49): "./song/ฮั่งเส็งรอบบ่าย 3 นาที.MP3",  # ฮั่งเส็งรอบบ่าย ก่อนปิด 3 นาที: 14:49

# ฮั่งเส็ง(บ่าย) VIP
datetime.time(15, 10): "./song/ฮั่งเส็ง(บ่าย) VIP 10 นาที.MP3",  # ฮั่งเส็ง(บ่าย) VIP ก่อนปิด 10 นาที: 15:10
datetime.time(15, 15): "./song/ฮั่งเส็ง(บ่าย) VIP 5 นาที.MP3",  # ฮั่งเส็ง(บ่าย) VIP ก่อนปิด 5 นาที: 15:15
datetime.time(15, 17): "./song/ฮั่งเส็ง(บ่าย) VIP 3 นาที.MP3",  # ฮั่งเส็ง(บ่าย) VIP ก่อนปิด 3 นาที: 15:17

# หวยลาว สตาร์
datetime.time(15, 30): "./song/หวยลาว สตาร์ 10 นาที.MP3",  # หวยลาว สตาร์ ก่อนปิด 10 นาที: 15:30
datetime.time(15, 35): "./song/หวยลาว สตาร์ 5 นาที.MP3",  # หวยลาว สตาร์ ก่อนปิด 5 นาที: 15:35
datetime.time(15, 37): "./song/หวยลาว สตาร์ 3 นาที.MP3",  # หวยลาว สตาร์ ก่อนปิด 3 นาที: 15:37

# หุ้นไทยพิเศษบ่าย
datetime.time(15, 35): "./song/หุ้นไทยพิเศษบ่าย 10 นาที.MP3",  # หุ้นไทยพิเศษบ่าย ก่อนปิด 10 นาที: 15:35
datetime.time(15, 40): "./song/หุ้นไทยพิเศษบ่าย 5 นาที.MP3",  # หุ้นไทยพิเศษบ่าย ก่อนปิด 5 นาที: 15:40
datetime.time(15, 42): "./song/หุ้นไทยพิเศษบ่าย 3 นาที.MP3",  # หุ้นไทยพิเศษบ่าย ก่อนปิด 3 นาที: 15:42

# หุ้นสิงคโปร์
datetime.time(15, 45): "./song/หุ้นสิงคโปร์ 10 นาที.MP3",  # หุ้นสิงคโปร์ ก่อนปิด 10 นาที: 15:45
datetime.time(15, 50): "./song/หุ้นสิงคโปร์ 5 นาที.MP3",  # หุ้นสิงคโปร์ ก่อนปิด 5 นาที: 15:50
datetime.time(15, 52): "./song/หุ้นสิงคโปร์ 3 นาที.MP3",  # หุ้นสิงคโปร์ ก่อนปิด 3 นาที: 15:52

# หุ้นไทยปิดเย็น
datetime.time(15, 55): "./song/หุ้นไทยปิดเย็น 10 นาที.MP3",  # หุ้นไทยปิดเย็น ก่อนปิด 10 นาที: 15:55
datetime.time(16, 0): "./song/หุ้นไทยปิดเย็น 5 นาที.MP3",  # หุ้นไทยปิดเย็น ก่อนปิด 5 นาที: 16:00
datetime.time(16, 2): "./song/หุ้นไทยปิดเย็น 3 นาที.MP3",  # หุ้นไทยปิดเย็น ก่อนปิด 3 นาที: 16:02

# หวยฮานอย กาชาด
datetime.time(16, 0): "./song/หวยฮานอย กาชาด 10 นาที.MP3",  # หวยฮานอย กาชาด ก่อนปิด 10 นาที: 16:00
datetime.time(16, 5): "./song/หวยฮานอย กาชาด 5 นาที.MP3",  # หวยฮานอย กาชาด ก่อนปิด 5 นาที: 16:05
datetime.time(16, 7): "./song/หวยฮานอย กาชาด 3 นาที.MP3",  # หวยฮานอย กาชาด ก่อนปิด 3 นาที: 16:07

# หุ้นอินเดีย
datetime.time(16, 40): "./song/หุ้นอินเดีย 10 นาที.MP3",  # หุ้นอินเดีย ก่อนปิด 10 นาที: 16:40
datetime.time(16, 45): "./song/หุ้นอินเดีย 5 นาที.MP3",  # หุ้นอินเดีย ก่อนปิด 5 นาที: 16:45
datetime.time(16, 47): "./song/หุ้นอินเดีย 3 นาที.MP3",  # หุ้นอินเดีย ก่อนปิด 3 นาที: 16:47

# สิงคโปร์ VIP
datetime.time(16, 50): "./song/สิงคโปร์ VIP 10 นาที.MP3",  # สิงคโปร์ VIP ก่อนปิด 10 นาที: 16:50
datetime.time(16, 55): "./song/สิงคโปร์ VIP 5 นาที.MP3",  # สิงคโปร์ VIP ก่อนปิด 5 นาที: 16:55
datetime.time(16, 57): "./song/สิงคโปร์ VIP 3 นาที.MP3",  # สิงคโปร์ VIP ก่อนปิด 3 นาที: 16:57

# ฮานอยสามัคคี
datetime.time(17, 0): "./song/ฮานอยสามัคคี 10 นาที.MP3",  # ฮานอยสามัคคี ก่อนปิด 10 นาที: 17:00
datetime.time(17, 5): "./song/ฮานอยสามัคคี 5 นาที.MP3",  # ฮานอยสามัคคี ก่อนปิด 5 นาที: 17:05
datetime.time(17, 7): "./song/ฮานอยสามัคคี 3 นาที.MP3",  # ฮานอยสามัคคี ก่อนปิด 3 นาที: 17:07

# ฮานอยพิเศษ
datetime.time(17, 2): "./song/ฮานอยพิเศษ 10 นาที.MP3",  # ฮานอยพิเศษ ก่อนปิด 10 นาที: 17:02
datetime.time(17, 7): "./song/ฮานอยพิเศษ 5 นาที.MP3",  # ฮานอยพิเศษ ก่อนปิด 5 นาที: 17:07
datetime.time(17, 9): "./song/ฮานอยพิเศษ 3 นาที.MP3",  # ฮานอยพิเศษ ก่อนปิด 3 นาที: 17:09

# หวยฮานอย
datetime.time(18, 2): "./song/หวยฮานอย 10 นาที.MP3",  # หวยฮานอย ก่อนปิด 10 นาที: 18:02
datetime.time(18, 7): "./song/หวยฮานอย 5 นาที.MP3",  # หวยฮานอย ก่อนปิด 5 นาที: 18:07
datetime.time(18, 9): "./song/หวยฮานอย 3 นาที.MP3",  # หวยฮานอย ก่อนปิด 3 นาที: 18:09

# หวยฮานอย VIP
datetime.time(19, 0): "./song/หวยฮานอย VIP 10 นาที.MP3",  # หวยฮานอย VIP ก่อนปิด 10 นาที: 19:00
datetime.time(19, 5): "./song/หวยฮานอย VIP 5 นาที.MP3",  # หวยฮานอย VIP ก่อนปิด 5 นาที: 19:05
datetime.time(19, 7): "./song/หวยฮานอย VIP 3 นาที.MP3",  # หวยฮานอย VIP ก่อนปิด 3 นาที: 19:07

# ฮานอยพัฒนา
datetime.time(19, 0): "./song/ฮานอยพัฒนา 10 นาที.MP3",  # ฮานอยพัฒนา ก่อนปิด 10 นาที: 19:00
datetime.time(19, 5): "./song/ฮานอยพัฒนา 5 นาที.MP3",  # ฮานอยพัฒนา ก่อนปิด 5 นาที: 19:05
datetime.time(19, 7): "./song/ฮานอยพัฒนา 3 นาที.MP3",  # ฮานอยพัฒนา ก่อนปิด 3 นาที: 19:07

# หวยลาว
datetime.time(20, 8): "./song/หวยลาว 10 นาที.MP3",  # หวยลาว ก่อนปิด 10 นาที: 20:08
datetime.time(20, 13): "./song/หวยลาว 5 นาที.MP3",  # หวยลาว ก่อนปิด 5 นาที: 20:13
datetime.time(20, 15): "./song/หวยลาว 3 นาที.MP3",  # หวยลาว ก่อนปิด 3 นาที: 20:15

# หวยลาวสามัคคี
datetime.time(20, 10): "./song/หวยลาวสามัคคี 10 นาที.MP3",  # หวยลาวสามัคคี ก่อนปิด 10 นาที: 20:10
datetime.time(20, 15): "./song/หวยลาวสามัคคี 5 นาที.MP3",  # หวยลาวสามัคคี ก่อนปิด 5 นาที: 20:15
datetime.time(20, 17): "./song/หวยลาวสามัคคี 3 นาที.MP3",  # หวยลาวสามัคคี ก่อนปิด 3 นาที: 20:17

# ลาวอาเซียน
datetime.time(20, 45): "./song/ลาวอาเซียน 10 นาที.MP3",  # ลาวอาเซียน ก่อนปิด 10 นาที: 20:45
datetime.time(20, 50): "./song/ลาวอาเซียน 5 นาที.MP3",  # ลาวอาเซียน ก่อนปิด 5 นาที: 20:50
datetime.time(20, 52): "./song/ลาวอาเซียน 3 นาที.MP3",  # ลาวอาเซียน ก่อนปิด 3 นาที: 20:52

# หวยลาว VIP
datetime.time(21, 10): "./song/หวยลาว VIP 10 นาที.MP3",  # หวยลาว VIP ก่อนปิด 10 นาที: 21:10
datetime.time(21, 15): "./song/หวยลาว VIP 5 นาที.MP3",  # หวยลาว VIP ก่อนปิด 5 นาที: 21:15
datetime.time(21, 17): "./song/หวยลาว VIP 3 นาที.MP3",  # หวยลาว VIP ก่อนปิด 3 นาที: 21:17

# หวยลาวสามัคคี VIP
datetime.time(21, 15): "./song/หวยลาวสามัคคี VIP 10 นาที.MP3",  # หวยลาวสามัคคี VIP ก่อนปิด 10 นาที: 21:15
datetime.time(21, 20): "./song/หวยลาวสามัคคี VIP 5 นาที.MP3",  # หวยลาวสามัคคี VIP ก่อนปิด 5 นาที: 21:20
datetime.time(21, 22): "./song/หวยลาวสามัคคี VIP 3 นาที.MP3",  # หวยลาวสามัคคี VIP ก่อนปิด 3 นาที: 21:22

# หวยลาว STAR VIP
datetime.time(21, 35): "./song/หวยลาว STAR VIP 10 นาที.MP3",  # หวยลาว STAR VIP ก่อนปิด 10 นาที: 21:35
datetime.time(21, 40): "./song/หวยลาว STAR VIP 5 นาที.MP3",  # หวยลาว STAR VIP ก่อนปิด 5 นาที: 21:40
datetime.time(21, 42): "./song/หวยลาว STAR VIP 3 นาที.MP3",  # หวยลาว STAR VIP ก่อนปิด 3 นาที: 21:42

# อังกฤษ VIP
datetime.time(21, 35): "./song/อังกฤษ VIP 10 นาที.MP3",  # อังกฤษ VIP ก่อนปิด 10 นาที: 21:35
datetime.time(21, 40): "./song/อังกฤษ VIP 5 นาที.MP3",  # อังกฤษ VIP ก่อนปิด 5 นาที: 21:40
datetime.time(21, 42): "./song/อังกฤษ VIP 3 นาที.MP3",  # อังกฤษ VIP ก่อนปิด 3 นาที: 21:42

# หวยฮานอย Extra
datetime.time(22, 0): "./song/หวยฮานอย Extra 10 นาที.MP3",  # หวยฮานอย Extra ก่อนปิด 10 นาที: 22:00
datetime.time(22, 5): "./song/หวยฮานอย Extra 5 นาที.MP3",  # หวยฮานอย Extra ก่อนปิด 5 นาที: 22:05
datetime.time(22, 7): "./song/หวยฮานอย Extra 3 นาที.MP3",  # หวยฮานอย Extra ก่อนปิด 3 นาที: 22:07

# หุ้นอังกฤษ
datetime.time(22, 5): "./song/หุ้นอังกฤษ 10 นาที.MP3",  # หุ้นอังกฤษ ก่อนปิด 10 นาที: 22:05
datetime.time(22, 10): "./song/หุ้นอังกฤษ 5 นาที.MP3",  # หุ้นอังกฤษ ก่อนปิด 5 นาที: 22:10
datetime.time(22, 12): "./song/หุ้นอังกฤษ 3 นาที.MP3",  # หุ้นอังกฤษ ก่อนปิด 3 นาที: 22:12

# หุ้นเยอรมัน
datetime.time(22, 5): "./song/หุ้นเยอรมัน 10 นาที.MP3",  # หุ้นเยอรมัน ก่อนปิด 10 นาที: 22:05
datetime.time(22, 10): "./song/หุ้นเยอรมัน 5 นาที.MP3",  # หุ้นเยอรมัน ก่อนปิด 5 นาที: 22:10
datetime.time(22, 12): "./song/หุ้นเยอรมัน 3 นาที.MP3",  # หุ้นเยอรมัน ก่อนปิด 3 นาที: 22:12

# หุ้นรัสเซีย
datetime.time(22, 20): "./song/หุ้นรัสเซีย 10 นาที.MP3",  # หุ้นรัสเซีย ก่อนปิด 10 นาที: 22:20
datetime.time(22, 25): "./song/หุ้นรัสเซีย 5 นาที.MP3",  # หุ้นรัสเซีย ก่อนปิด 5 นาที: 22:25
datetime.time(22, 27): "./song/หุ้นรัสเซีย 3 นาที.MP3",  # หุ้นรัสเซีย ก่อนปิด 3 นาที: 22:27

# เยอรมัน VIP
datetime.time(22, 35): "./song/เยอรมัน VIP 10 นาที.MP3",  # เยอรมัน VIP ก่อนปิด 10 นาที: 22:35
datetime.time(22, 40): "./song/เยอรมัน VIP 5 นาที.MP3",  # เยอรมัน VIP ก่อนปิด 5 นาที: 22:40
datetime.time(22, 42): "./song/เยอรมัน VIP 3 นาที.MP3",  # เยอรมัน VIP ก่อนปิด 3 นาที: 22:40

# หวยลาว กาชาด
datetime.time(23, 15): "./song/หวยลาว กาชาด 10 นาที.MP3",  # หวยลาว กาชาด ก่อนปิด 10 นาที: 23:15
datetime.time(23, 20): "./song/หวยลาว กาชาด 5 นาที.MP3",  # หวยลาว กาชาด ก่อนปิด 5 นาที: 23:20
datetime.time(23, 22): "./song/หวยลาว กาชาด 3 นาที.MP3",  # หวยลาว กาชาด ก่อนปิด 3 นาที: 23:22

# รัสเซีย VIP
datetime.time(23, 35): "./song/รัสเซีย VIP 10 นาที.MP3",  # รัสเซีย VIP ก่อนปิด 10 นาที: 23:35
datetime.time(23, 40): "./song/รัสเซีย VIP 5 นาที.MP3",  # รัสเซีย VIP ก่อนปิด 5 นาที: 23:40
datetime.time(23, 42): "./song/รัสเซีย VIP 3 นาที.MP3",  # รัสเซีย VIP ก่อนปิด 3 นาที: 23:42

# หวยดาวโจนส์ VIP
datetime.time(0, 0): "./song/หวยดาวโจนส์ VIP 10 นาที.MP3",  # หวยดาวโจนส์ VIP ก่อนปิด 10 นาที: 00:00
datetime.time(0, 5): "./song/หวยดาวโจนส์ VIP 5 นาที.MP3",  # หวยดาวโจนส์ VIP ก่อนปิด 5 นาที: 00:05
datetime.time(0, 7): "./song/หวยดาวโจนส์ VIP 3 นาที.MP3",  # หวยดาวโจนส์ VIP ก่อนปิด 3 นาที: 00:07

# หวยดาวโจนส์ STAR
datetime.time(0, 55): "./song/หวยดาวโจนส์ STAR 10 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 10 นาที: 00:55
datetime.time(1, 0): "./song/หวยดาวโจนส์ STAR 5 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 5 นาที: 01:00
datetime.time(1, 2): "./song/หวยดาวโจนส์ STAR 3 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 3 นาที: 01:02


# หวยดาวโจนส์ STAR
datetime.time(1, 55): "./song/หวยดาวโจนส์ STAR 10 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 10 นาที: 00:55
datetime.time(2, 00): "./song/หวยดาวโจนส์ STAR 5 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 5 นาที: 01:00
datetime.time(1, 57): "./song/หวยดาวโจนส์ STAR 3 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 3 นาที: 01:02
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
