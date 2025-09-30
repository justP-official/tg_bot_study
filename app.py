import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from handlers.admin_private import admin_router
# from common.bot_cmds_list import private

from midlewares.db import DataBaseSession

# ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

bot = Bot(token=os.getenv("TG_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = []

dispatcher = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)


dispatcher.include_router(user_private_router)
dispatcher.include_router(user_group_router)
dispatcher.include_router(admin_router)


async def on_startup(bot):
    # await drop_db()

    await create_db()


async def on_shutdown(bot):
    print("Бот лёг")


async def main():
    dispatcher.startup.register(on_startup)  # Функция, которая срабатывает при запуске бота
    dispatcher.shutdown.register(on_shutdown)  # Функция, которая срабатывает при выключении бота

    dispatcher.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)

    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())  # -- Если нужно удалить команды
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    
    await dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())


asyncio.run(main())
