from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.enums import ParseMode

from filters.chat_types import ChatTypeFilter
from keyboards import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, я виртуальный помощник", 
                         reply_markup=reply.start_keyboard_with_builder_2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что вас интересует?"
                         ))


# @user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer("__Меню:__", # курсив
                         reply_markup=reply.del_keyboard,
                         parse_mode=ParseMode.MARKDOWN_V2)


@user_private_router.message(F.text.lower() == "о магазине")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("<b>О нас:</b>", # жирный
                         parse_mode=ParseMode.HTML)


@user_private_router.message(F.text.lower() == "варианты оплаты")
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    await message.answer("_Оплата:_", # курсив
                         parse_mode=ParseMode.MARKDOWN)


@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    await message.answer("Доставка:",
                         reply_markup=reply.test_keyboard)


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer("номер получен")
    # await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer("локация получена")
    # await message.answer(str(message.location))


# @user_private_router.message(F.text)
# async def magick_cmd(message: types.Message):
#     await message.answer("Magick!")
