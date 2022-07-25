from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot('5211004300:AAFDhpRH79hS7zFcux64xqMinAWbgc-DSyA')
dp = Dispatcher(bot, storage=storage)





