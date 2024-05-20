import asyncio

from aiogram import Bot, Dispatcher, filters, types

from config import API_KEY
from main import payments
import json

bot = Bot(token=API_KEY)
dp = Dispatcher()


@dp.message(filters.CommandStart())
async def start_command(message: types.Message):
    await message.answer(f"Привет {message.from_user.username}")


@dp.message()
async def get_payments(message: types.Message):
    message_dict = json.loads(message.text)
    dt_from = message_dict.get("dt_from")
    dt_upto = message_dict.get("dt_upto")
    group_type = message_dict.get("group_type")
    result = payments(dt_from, dt_upto, group_type)
    await message.answer(text=str(result).replace("'", '"'))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
