# - *- coding: utf- 8 - *-
import sys
from os import environ
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
load_dotenv()

token = environ.get("TOKEN")
if token:
	bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
	dp = Dispatcher(bot, storage=MemoryStorage())
else:
	print("Пожалуйста, укажите токен для бота как переменную окружения и попробуйте снова.")
	sys.exit(0)
