from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import sys
from aiogram.contrib.fsm_storage.memory import MemoryStorage

sys.path.append(r".\music_downloader\downloader.py")
from music_downloader import downloader

sys.path.append(r".chatgpt\openai_bot.py")
from chatgpt import openai_bot

load_dotenv()

ai = openai_bot.ChatGPT()

music = downloader.M3U8Downloader(login=os.getenv("LOGIN_VK"), password=os.getenv("PASSWORD_VK"))
bot = Bot(os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
