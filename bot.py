from aiogram import Bot
from decouple import config
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token=config('token'))
dp = Dispatcher(bot, storage=storage)

