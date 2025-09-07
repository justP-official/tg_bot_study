from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, я виртуальный помощник")


# @user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer("Menu:")


@user_private_router.message(F.text.lower() == "о нас")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("О нас:")


@user_private_router.message(F.text.lower() == "варианты оплаты")
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    await message.answer("Оплата:")


@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    await message.answer("Доставка:")


@user_private_router.message(F.text)
async def magick_cmd(message: types.Message):
    await message.answer("Magick!")
