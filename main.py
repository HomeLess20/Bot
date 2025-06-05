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
datetime.time(8, 14): "./song/หวยลาว Extra 10 นาที.MP3",  # หวยลาว Extra ก่อนปิด 10 นาที: 08:14
datetime.time(8, 19): "./song/หวยลาว Extra 5 นาที.MP3",  # หวยลาว Extra ก่อนปิด 5 นาที: 08:19
datetime.time(8, 21): "./song/หวยลาว Extra 3 นาที.MP3",  # หวยลาว Extra ก่อนปิด 3 นาที: 08:21

# นิเคอิ(เช้า) VIP
datetime.time(8, 49): "./song/นิเคอิ(เช้า) VIP 10 นาที.MP3",  # นิเคอิ(เช้า) VIP ก่อนปิด 10 นาที: 08:49
datetime.time(8, 54): "./song/นิเคอิ(เช้า) VIP 5 นาที.MP3",  # นิเคอิ(เช้า) VIP ก่อนปิด 5 นาที: 08:54
datetime.time(8, 56): "./song/นิเคอิ(เช้า) VIP 3 นาที.MP3",  # นิเคอิ(เช้า) VIP ก่อนปิด 3 นาที: 08:56

# ฮานอยอาเซียน
datetime.time(8, 59): "./song/ฮานอยอาเซียน 10 นาที.MP3",  # ฮานอยอาเซียน ก่อนปิด 10 นาที: 08:59
datetime.time(9, 4): "./song/ฮานอยอาเซียน 5 นาที.MP3",  # ฮานอยอาเซียน ก่อนปิด 5 นาที: 09:04
datetime.time(9, 6): "./song/ฮานอยอาเซียน 3 นาที.MP3",  # ฮานอยอาเซียน ก่อนปิด 3 นาที: 09:06

# นิเคอิ รอบเช้า
datetime.time(9, 11): "./song/นิเคอิ รอบเช้า 10 นาที.MP3",  # นิเคอิ รอบเช้า ก่อนปิด 10 นาที: 09:11
datetime.time(9, 16): "./song/นิเคอิ รอบเช้า 5 นาที.MP3",  # นิเคอิ รอบเช้า ก่อนปิด 5 นาที: 09:16
datetime.time(9, 18): "./song/นิเคอิ รอบเช้า 3 นาที.MP3",  # นิเคอิ รอบเช้า ก่อนปิด 3 นาที: 09:18

# จีน(เช้า) VIP
datetime.time(9, 49): "./song/จีน(เช้า) VIP 10 นาที.MP3",  # จีน(เช้า) VIP ก่อนปิด 10 นาที: 09:49
datetime.time(9, 54): "./song/จีน(เช้า) VIP 5 นาที.MP3",  # จีน(เช้า) VIP ก่อนปิด 5 นาที: 09:54
datetime.time(9, 56): "./song/จีน(เช้า) VIP 3 นาที.MP3",  # จีน(เช้า) VIP ก่อนปิด 3 นาที: 09:56

# จีนรอบเช้า
datetime.time(10, 9): "./song/จีนรอบเช้า 10 นาที.MP3",  # จีนรอบเช้า ก่อนปิด 10 นาที: 10:09
datetime.time(10, 14): "./song/จีนรอบเช้า 5 นาที.MP3",  # จีนรอบเช้า ก่อนปิด 5 นาที: 10:14
datetime.time(10, 16): "./song/จีนรอบเช้า 3 นาที.MP3",  # จีนรอบเช้า ก่อนปิด 3 นาที: 10:16

# หวยลาว TV
datetime.time(10, 14): "./song/หวยลาว TV 10 นาที.MP3",  # หวยลาว TV ก่อนปิด 10 นาที: 10:14
datetime.time(10, 19): "./song/หวยลาว TV 5 นาที.MP3",  # หวยลาว TV ก่อนปิด 5 นาที: 10:19
datetime.time(10, 21): "./song/หวยลาว TV 3 นาที.MP3",  # หวยลาว TV ก่อนปิด 3 นาที: 10:21

# ฮั่งเส็ง(เช้า) VIP
datetime.time(10, 19): "./song/ฮั่งเส็ง(เช้า) VIP 10 นาที.MP3",  # ฮั่งเส็ง(เช้า) VIP ก่อนปิด 10 นาที: 10:19
datetime.time(10, 24): "./song/ฮั่งเส็ง(เช้า) VIP 5 นาที.MP3",  # ฮั่งเส็ง(เช้า) VIP ก่อนปิด 5 นาที: 10:24
datetime.time(10, 26): "./song/ฮั่งเส็ง(เช้า) VIP 3 นาที.MP3",  # ฮั่งเส็ง(เช้า) VIP ก่อนปิด 3 นาที: 10:26

# ฮั่งเส็งรอบเช้า
datetime.time(10, 41): "./song/ฮั่งเส็งรอบเช้า 10 นาที.MP3",  # ฮั่งเส็งรอบเช้า ก่อนปิด 10 นาที: 10:41
datetime.time(10, 46): "./song/ฮั่งเส็งรอบเช้า 5 นาที.MP3",  # ฮั่งเส็งรอบเช้า ก่อนปิด 5 นาที: 10:46
datetime.time(10, 48): "./song/ฮั่งเส็งรอบเช้า 3 นาที.MP3",  # ฮั่งเส็งรอบเช้า ก่อนปิด 3 นาที: 10:48

# ฮานอย HD
datetime.time(10, 59): "./song/ฮานอย HD 10 นาที.MP3",  # ฮานอย HD ก่อนปิด 10 นาที: 10:59
datetime.time(11, 4): "./song/ฮานอย HD 5 นาที.MP3",  # ฮานอย HD ก่อนปิด 5 นาที: 11:04
datetime.time(11, 6): "./song/ฮานอย HD 3 นาที.MP3",  # ฮานอย HD ก่อนปิด 3 นาที: 11:06

# ไต้หวัน VIP
datetime.time(11, 19): "./song/ไต้หวัน VIP 10 นาที.MP3",  # ไต้หวัน VIP ก่อนปิด 10 นาที: 11:19
datetime.time(11, 24): "./song/ไต้หวัน VIP 5 นาที.MP3",  # ไต้หวัน VIP ก่อนปิด 5 นาที: 11:24
datetime.time(11, 26): "./song/ไต้หวัน VIP 3 นาที.MP3",  # ไต้หวัน VIP ก่อนปิด 3 นาที: 11:26

# หุ้นไทยพิเศษเที่ยง
datetime.time(11, 34): "./song/หุ้นไทยพิเศษเที่ยง 10 นาที.MP3",  # หุ้นไทยพิเศษเที่ยง ก่อนปิด 10 นาที: 11:34
datetime.time(11, 39): "./song/หุ้นไทยพิเศษเที่ยง 5 นาที.MP3",  # หุ้นไทยพิเศษเที่ยง ก่อนปิด 5 นาที: 11:39
datetime.time(11, 41): "./song/หุ้นไทยพิเศษเที่ยง 3 นาที.MP3",  # หุ้นไทยพิเศษเที่ยง ก่อนปิด 3 นาที: 11:41

# ฮานอย สตาร์
datetime.time(11, 59): "./song/ฮานอย สตาร์ 10 นาที.MP3",  # ฮานอย สตาร์ ก่อนปิด 10 นาที: 11:59
datetime.time(12, 4): "./song/ฮานอย สตาร์ 5 นาที.MP3",  # ฮานอย สตาร์ ก่อนปิด 5 นาที: 12:04
datetime.time(12, 6): "./song/ฮานอย สตาร์ 3 นาที.MP3",  # ฮานอย สตาร์ ก่อนปิด 3 นาที: 12:06

# หุ้นไต้หวัน
datetime.time(11, 59): "./song/หุ้นไต้หวัน 10 นาที.MP3",  # หุ้นไต้หวัน ก่อนปิด 10 นาที: 11:59
datetime.time(12, 4): "./song/หุ้นไต้หวัน 5 นาที.MP3",  # หุ้นไต้หวัน ก่อนปิด 5 นาที: 12:04
datetime.time(12, 6): "./song/หุ้นไต้หวัน 3 นาที.MP3",  # หุ้นไต้หวัน ก่อนปิด 3 นาที: 12:06

# เกาหลี VIP
datetime.time(12, 19): "./song/เกาหลี VIP 10 นาที.MP3",  # เกาหลี VIP ก่อนปิด 10 นาที: 12:19
datetime.time(12, 24): "./song/เกาหลี VIP 5 นาที.MP3",  # เกาหลี VIP ก่อนปิด 5 นาที: 12:24
datetime.time(12, 26): "./song/เกาหลี VIP 3 นาที.MP3",  # เกาหลี VIP ก่อนปิด 3 นาที: 12:26

# หุ้นเกาหลี
datetime.time(12, 34): "./song/หุ้นเกาหลี 10 นาที.MP3",  # หุ้นเกาหลี ก่อนปิด 10 นาที: 12:34
datetime.time(12, 39): "./song/หุ้นเกาหลี 5 นาที.MP3",  # หุ้นเกาหลี ก่อนปิด 5 นาที: 12:39
datetime.time(12, 41): "./song/หุ้นเกาหลี 3 นาที.MP3",  # หุ้นเกาหลี ก่อนปิด 3 นาที: 12:41

# นิเคอิ รอบบ่าย
datetime.time(12, 41): "./song/นิเคอิ รอบบ่าย 10 นาที.MP3",  # นิเคอิ รอบบ่าย ก่อนปิด 10 นาที: 12:41
datetime.time(12, 46): "./song/นิเคอิ รอบบ่าย 5 นาที.MP3",  # นิเคอิ รอบบ่าย ก่อนปิด 5 นาที: 12:46
datetime.time(12, 48): "./song/นิเคอิ รอบบ่าย 3 นาที.MP3",  # นิเคอิ รอบบ่าย ก่อนปิด 3 นาที: 12:48

# นิเคอิ(บ่าย) VIP
datetime.time(13, 9): "./song/นิเคอิ(บ่าย) VIP 10 นาที.MP3",  # นิเคอิ(บ่าย) VIP ก่อนปิด 10 นาที: 13:09
datetime.time(13, 14): "./song/นิเคอิ(บ่าย) VIP 5 นาที.MP3",  # นิเคอิ(บ่าย) VIP ก่อนปิด 5 นาที: 13:14
datetime.time(13, 16): "./song/นิเคอิ(บ่าย) VIP 3 นาที.MP3",  # นิเคอิ(บ่าย) VIP ก่อนปิด 3 นาที: 13:16

# หวยลาว HD
datetime.time(13, 29): "./song/หวยลาว HD 10 นาที.MP3",  # หวยลาว HD ก่อนปิด 10 นาที: 13:29
datetime.time(13, 34): "./song/หวยลาว HD 5 นาที.MP3",  # หวยลาว HD ก่อนปิด 5 นาที: 13:34
datetime.time(13, 36): "./song/หวยลาว HD 3 นาที.MP3",  # หวยลาว HD ก่อนปิด 3 นาที: 13:36

# จีนรอบบ่าย
datetime.time(13, 34): "./song/จีนรอบบ่าย 10 นาที.MP3",  # จีนรอบบ่าย ก่อนปิด 10 นาที: 13:34
datetime.time(13, 39): "./song/จีนรอบบ่าย 5 นาที.MP3",  # จีนรอบบ่าย ก่อนปิด 5 นาที: 13:39
datetime.time(13, 41): "./song/จีนรอบบ่าย 3 นาที.MP3",  # จีนรอบบ่าย ก่อนปิด 3 นาที: 13:41

# หวยฮานอย TV
datetime.time(13, 59): "./song/หวยฮานอย TV 10 นาที.MP3",  # หวยฮานอย TV ก่อนปิด 10 นาที: 13:59
datetime.time(14, 4): "./song/หวยฮานอย TV 5 นาที.MP3",  # หวยฮานอย TV ก่อนปิด 5 นาที: 14:04
datetime.time(14, 6): "./song/หวยฮานอย TV 3 นาที.MP3",  # หวยฮานอย TV ก่อนปิด 3 นาที: 14:06

# จีน(บ่าย) VIP
datetime.time(14, 9): "./song/จีน(บ่าย) VIP 10 นาที.MP3",  # จีน(บ่าย) VIP ก่อนปิด 10 นาที: 14:09
datetime.time(14, 14): "./song/จีน(บ่าย) VIP 5 นาที.MP3",  # จีน(บ่าย) VIP ก่อนปิด 5 นาที: 14:14
datetime.time(14, 16): "./song/จีน(บ่าย) VIP 3 นาที.MP3",  # จีน(บ่าย) VIP ก่อนปิด 3 นาที: 14:16

# ฮั่งเส็งรอบบ่าย
datetime.time(14, 41): "./song/ฮั่งเส็งรอบบ่าย 10 นาที.MP3",  # ฮั่งเส็งรอบบ่าย ก่อนปิด 10 นาที: 14:41
datetime.time(14, 46): "./song/ฮั่งเส็งรอบบ่าย 5 นาที.MP3",  # ฮั่งเส็งรอบบ่าย ก่อนปิด 5 นาที: 14:46
datetime.time(14, 48): "./song/ฮั่งเส็งรอบบ่าย 3 นาที.MP3",  # ฮั่งเส็งรอบบ่าย ก่อนปิด 3 นาที: 14:48

# ฮั่งเส็ง(บ่าย) VIP
datetime.time(15, 9): "./song/ฮั่งเส็ง(บ่าย) VIP 10 นาที.MP3",  # ฮั่งเส็ง(บ่าย) VIP ก่อนปิด 10 นาที: 15:09
datetime.time(15, 14): "./song/ฮั่งเส็ง(บ่าย) VIP 5 นาที.MP3",  # ฮั่งเส็ง(บ่าย) VIP ก่อนปิด 5 นาที: 15:14
datetime.time(15, 16): "./song/ฮั่งเส็ง(บ่าย) VIP 3 นาที.MP3",  # ฮั่งเส็ง(บ่าย) VIP ก่อนปิด 3 นาที: 15:16

# หวยลาว สตาร์
datetime.time(15, 29): "./song/หวยลาว สตาร์ 10 นาที.MP3",  # หวยลาว สตาร์ ก่อนปิด 10 นาที: 15:29
datetime.time(15, 34): "./song/หวยลาว สตาร์ 5 นาที.MP3",  # หวยลาว สตาร์ ก่อนปิด 5 นาที: 15:34
datetime.time(15, 36): "./song/หวยลาว สตาร์ 3 นาที.MP3",  # หวยลาว สตาร์ ก่อนปิด 3 นาที: 15:36

# หุ้นไทยพิเศษบ่าย
datetime.time(15, 34): "./song/หุ้นไทยพิเศษบ่าย 10 นาที.MP3",  # หุ้นไทยพิเศษบ่าย ก่อนปิด 10 นาที: 15:34
datetime.time(15, 39): "./song/หุ้นไทยพิเศษบ่าย 5 นาที.MP3",  # หุ้นไทยพิเศษบ่าย ก่อนปิด 5 นาที: 15:39
datetime.time(15, 41): "./song/หุ้นไทยพิเศษบ่าย 3 นาที.MP3",  # หุ้นไทยพิเศษบ่าย ก่อนปิด 3 นาที: 15:4

# หุ้นสิงคโปร์
datetime.time(15, 44): "./song/หุ้นสิงคโปร์ 10 นาที.MP3",  # หุ้นสิงคโปร์ ก่อนปิด 10 นาที: 15:44
datetime.time(15, 49): "./song/หุ้นสิงคโปร์ 5 นาที.MP3",  # หุ้นสิงคโปร์ ก่อนปิด 5 นาที: 15:49
datetime.time(15, 51): "./song/หุ้นสิงคโปร์ 3 นาที.MP3",  # หุ้นสิงคโปร์ ก่อนปิด 3 นาที: 15:51

# หุ้นไทยปิดเย็น
datetime.time(15, 54): "./song/หุ้นไทยปิดเย็น 10 นาที.MP3",  # หุ้นไทยปิดเย็น ก่อนปิด 10 นาที: 15:54
datetime.time(15, 59): "./song/หุ้นไทยปิดเย็น 5 นาที.MP3",  # หุ้นไทยปิดเย็น ก่อนปิด 5 นาที: 15:59
datetime.time(16, 1): "./song/หุ้นไทยปิดเย็น 3 นาที.MP3",  # หุ้นไทยปิดเย็น ก่อนปิด 3 นาที: 16:01

# หวยฮานอย กาชาด
datetime.time(15, 59): "./song/หวยฮานอย กาชาด 10 นาที.MP3",  # หวยฮานอย กาชาด ก่อนปิด 10 นาที: 15:59
datetime.time(16, 4): "./song/หวยฮานอย กาชาด 5 นาที.MP3",  # หวยฮานอย กาชาด ก่อนปิด 5 นาที: 16:04
datetime.time(16, 6): "./song/หวยฮานอย กาชาด 3 นาที.MP3",  # หวยฮานอย กาชาด ก่อนปิด 3 นาที: 16:06

# หุ้นอินเดีย
datetime.time(16, 39): "./song/หุ้นอินเดีย 10 นาที.MP3",  # หุ้นอินเดีย ก่อนปิด 10 นาที: 16:39
datetime.time(16, 44): "./song/หุ้นอินเดีย 5 นาที.MP3",  # หุ้นอินเดีย ก่อนปิด 5 นาที: 16:44
datetime.time(16, 46): "./song/หุ้นอินเดีย 3 นาที.MP3",  # หุ้นอินเดีย ก่อนปิด 3 นาที: 16:46

# สิงคโปร์ VIP
datetime.time(16, 49): "./song/สิงคโปร์ VIP 10 นาที.MP3",  # สิงคโปร์ VIP ก่อนปิด 10 นาที: 16:49
datetime.time(16, 54): "./song/สิงคโปร์ VIP 5 นาที.MP3",  # สิงคโปร์ VIP ก่อนปิด 5 นาที: 16:54
datetime.time(16, 56): "./song/สิงคโปร์ VIP 3 นาที.MP3",  # สิงคโปร์ VIP ก่อนปิด 3 นาที: 16:56

# ฮานอยสามัคคี
datetime.time(16, 59): "./song/ฮานอยสามัคคี 10 นาที.MP3",  # ฮานอยสามัคคี ก่อนปิด 10 นาที: 16:59
datetime.time(17, 4): "./song/ฮานอยสามัคคี 5 นาที.MP3",  # ฮานอยสามัคคี ก่อนปิด 5 นาที: 17:04
datetime.time(17, 6): "./song/ฮานอยสามัคคี 3 นาที.MP3",  # ฮานอยสามัคคี ก่อนปิด 3 นาที: 17:06

# ฮานอยพิเศษ
datetime.time(17, 1): "./song/ฮานอยพิเศษ 10 นาที.MP3",  # ฮานอยพิเศษ ก่อนปิด 10 นาที: 17:01
datetime.time(17, 6): "./song/ฮานอยพิเศษ 5 นาที.MP3",  # ฮานอยพิเศษ ก่อนปิด 5 นาที: 17:06
datetime.time(17, 8): "./song/ฮานอยพิเศษ 3 นาที.MP3",  # ฮานอยพิเศษ ก่อนปิด 3 นาที: 17:08

# หวยฮานอย
datetime.time(18, 1): "./song/หวยฮานอย 10 นาที.MP3",  # หวยฮานอย ก่อนปิด 10 นาที: 18:01
datetime.time(18, 6): "./song/หวยฮานอย 5 นาที.MP3",  # หวยฮานอย ก่อนปิด 5 นาที: 18:06
datetime.time(18, 8): "./song/หวยฮานอย 3 นาที.MP3",  # หวยฮานอย ก่อนปิด 3 นาที: 18:08

# หวยฮานอย VIP # ฮานอยพัฒนา
datetime.time(18, 59): "./song/หวยฮานอย VIP 10 นาที.MP3",  # หวยฮานอย VIP ก่อนปิด 10 นาที: 18:59
datetime.time(19, 4): "./song/หวยฮานอย VIP 5 นาที.MP3",  # หวยฮานอย VIP ก่อนปิด 5 นาที: 19:04
datetime.time(19, 6): "./song/หวยฮานอย VIP 3 นาที.MP3",  # หวยฮานอย VIP ก่อนปิด 3 นาที: 19:06

# หวยลาว
datetime.time(20, 7): "./song/หวยลาว 10 นาที.MP3",  # หวยลาว ก่อนปิด 10 นาที: 20:07
datetime.time(20, 12): "./song/หวยลาว 5 นาที.MP3",  # หวยลาว ก่อนปิด 5 นาที: 20:12
datetime.time(20, 14): "./song/หวยลาว 3 นาที.MP3",  # หวยลาว ก่อนปิด 3 นาที: 20:14

# หวยลาวสามัคคี
datetime.time(20, 9): "./song/หวยลาวสามัคคี 10 นาที.MP3",  # หวยลาวสามัคคี ก่อนปิด 10 นาที: 20:09
datetime.time(20, 14): "./song/หวยลาวสามัคคี 5 นาที.MP3",  # หวยลาวสามัคคี ก่อนปิด 5 นาที: 20:14
datetime.time(20, 16): "./song/หวยลาวสามัคคี 3 นาที.MP3",  # หวยลาวสามัคคี ก่อนปิด 3 นาที: 20:16

# ลาวอาเซียน
datetime.time(20, 44): "./song/ลาวอาเซียน 10 นาที.MP3",  # ลาวอาเซียน ก่อนปิด 10 นาที: 20:44
datetime.time(20, 49): "./song/ลาวอาเซียน 5 นาที.MP3",  # ลาวอาเซียน ก่อนปิด 5 นาที: 20:49
datetime.time(20, 51): "./song/ลาวอาเซียน 3 นาที.MP3",  # ลาวอาเซียน ก่อนปิด 3 นาที: 20:51

# หวยลาว VIP
datetime.time(21, 9): "./song/หวยลาว VIP 10 นาที.MP3",  # หวยลาว VIP ก่อนปิด 10 นาที: 21:09
datetime.time(21, 14): "./song/หวยลาว VIP 5 นาที.MP3",  # หวยลาว VIP ก่อนปิด 5 นาที: 21:14
datetime.time(21, 16): "./song/หวยลาว VIP 3 นาที.MP3",  # หวยลาว VIP ก่อนปิด 3 นาที: 21:16

# หวยลาวสามัคคี VIP
datetime.time(21, 14): "./song/หวยลาวสามัคคี VIP 10 นาที.MP3",  # หวยลาวสามัคคี VIP ก่อนปิด 10 นาที: 21:14
datetime.time(21, 19): "./song/หวยลาวสามัคคี VIP 5 นาที.MP3",  # หวยลาวสามัคคี VIP ก่อนปิด 5 นาที: 21:19
datetime.time(21, 21): "./song/หวยลาวสามัคคี VIP 3 นาที.MP3",  # หวยลาวสามัคคี VIP ก่อนปิด 3 นาที: 21:21

# หวยลาว STAR VIP # อังกฤษ VIP
datetime.time(21, 34): "./song/หวยลาว STAR VIP 10 นาที.MP3",  # หวยลาว STAR VIP ก่อนปิด 10 นาที: 21:34
datetime.time(21, 39): "./song/หวยลาว STAR VIP 5 นาที.MP3",  # หวยลาว STAR VIP ก่อนปิด 5 นาที: 21:39
datetime.time(21, 41): "./song/หวยลาว STAR VIP 3 นาที.MP3",  # หวยลาว STAR VIP ก่อนปิด 3 นาที: 21:41

# หวยฮานอย Extra
datetime.time(21, 59): "./song/หวยฮานอย Extra 10 นาที.MP3",  # หวยฮานอย Extra ก่อนปิด 10 นาที: 21:59
datetime.time(22, 4): "./song/หวยฮานอย Extra 5 นาที.MP3",  # หวยฮานอย Extra ก่อนปิด 5 นาที: 22:04
datetime.time(22, 6): "./song/หวยฮานอย Extra 3 นาที.MP3",  # หวยฮานอย Extra ก่อนปิด 3 นาที: 22:06

# หุ้นอังกฤษ
datetime.time(22, 4): "./song/หุ้นอังกฤษ 10 นาที.MP3",  # หุ้นอังกฤษ ก่อนปิด 10 นาที: 22:04
datetime.time(22, 9): "./song/หุ้นอังกฤษ 5 นาที.MP3",  # หุ้นอังกฤษ ก่อนปิด 5 นาที: 22:09
datetime.time(22, 11): "./song/หุ้นอังกฤษ 3 นาที.MP3",  # หุ้นอังกฤษ ก่อนปิด 3 นาที: 22:11

# หุ้นเยอรมัน
datetime.time(22, 4): "./song/หุ้นเยอรมัน 10 นาที.MP3",  # หุ้นเยอรมัน ก่อนปิด 10 นาที: 22:04
datetime.time(22, 9): "./song/หุ้นเยอรมัน 5 นาที.MP3",  # หุ้นเยอรมัน ก่อนปิด 5 นาที: 22:09
datetime.time(22, 11): "./song/หุ้นเยอรมัน 3 นาที.MP3",  # หุ้นเยอรมัน ก่อนปิด 3 นาที: 22:11

# หุ้นรัสเซีย
datetime.time(22, 19): "./song/หุ้นรัสเซีย 10 นาที.MP3",  # หุ้นรัสเซีย ก่อนปิด 10 นาที: 22:19
datetime.time(22, 24): "./song/หุ้นรัสเซีย 5 นาที.MP3",  # หุ้นรัสเซีย ก่อนปิด 5 นาที: 22:24
datetime.time(22, 26): "./song/หุ้นรัสเซีย 3 นาที.MP3",  # หุ้นรัสเซีย ก่อนปิด 3 นาที: 22:26
# เยอรมัน VIP
datetime.time(22, 34): "./song/เยอรมัน VIP 10 นาที.MP3",  # เยอรมัน VIP ก่อนปิด 10 นาที: 22:34
datetime.time(22, 39): "./song/เยอรมัน VIP 5 นาที.MP3",  # เยอรมัน VIP ก่อนปิด 5 นาที: 22:39
datetime.time(22, 41): "./song/เยอรมัน VIP 3 นาที.MP3",  # เยอรมัน VIP ก่อนปิด 3 นาที: 22:41

# หวยลาว กาชาด
datetime.time(23, 14): "./song/หวยลาว กาชาด 10 นาที.MP3",  # หวยลาว กาชาด ก่อนปิด 10 นาที: 23:14
datetime.time(23, 19): "./song/หวยลาว กาชาด 5 นาที.MP3",  # หวยลาว กาชาด ก่อนปิด 5 นาที: 23:19
datetime.time(23, 21): "./song/หวยลาว กาชาด 3 นาที.MP3",  # หวยลาว กาชาด ก่อนปิด 3 นาที: 23:21

# รัสเซีย VIP
datetime.time(23, 34): "./song/รัสเซีย VIP 10 นาที.MP3",  # รัสเซีย VIP ก่อนปิด 10 นาที: 23:34
datetime.time(23, 39): "./song/รัสเซีย VIP 5 นาที.MP3",  # รัสเซีย VIP ก่อนปิด 5 นาที: 23:39
datetime.time(23, 41): "./song/รัสเซีย VIP 3 นาที.MP3",  # รัสเซีย VIP ก่อนปิด 3 นาที: 23:41

# หวยดาวโจนส์ VIP
datetime.time(23, 59): "./song/หวยดาวโจนส์ VIP 10 นาที.MP3",  # หวยดาวโจนส์ VIP ก่อนปิด 10 นาที: 23:59
datetime.time(0, 4): "./song/หวยดาวโจนส์ VIP 5 นาที.MP3",  # หวยดาวโจนส์ VIP ก่อนปิด 5 นาที: 00:04
datetime.time(0, 6): "./song/หวยดาวโจนส์ VIP 3 นาที.MP3",  # หวยดาวโจนส์ VIP ก่อนปิด 3 นาที: 00:06

# หวยดาวโจนส์ STAR
datetime.time(0, 54): "./song/หวยดาวโจนส์ STAR 10 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 10 นาที: 00:54
datetime.time(0, 59): "./song/หวยดาวโจนส์ STAR 5 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 5 นาที: 00:59
datetime.time(1, 1): "./song/หวยดาวโจนส์ STAR 3 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 3 นาที: 01:01


# หวยดาวโจนส์ STAR
datetime.time(1, 54): "./song/หวยดาวโจนส์ STAR 10 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 10 นาที: 01:54
datetime.time(1, 59): "./song/หวยดาวโจนส์ STAR 5 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 5 นาที: 01:59
datetime.time(1, 56): "./song/หวยดาวโจนส์ STAR 3 นาที.MP3",  # หวยดาวโจนส์ STAR ก่อนปิด 3 นาที: 01:56
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
