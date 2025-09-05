import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TG_TOKEN"))

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Start")


@dispatcher.message()
async def echo(message: types.Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Echo:")
    await message.answer(message.text)
    await message.reply(message.text)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


asyncio.run(main())
