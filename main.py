from aiogram import executor
from hundars import dp


if __name__ == '__main__':
    executor.Executor(dp, skip_updates=True).start_polling()

