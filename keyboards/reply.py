from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="О магазине"),
        ],
        [
            KeyboardButton(text="Варианты доставки"),
            KeyboardButton(text="Способы оплаты"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

del_keyboard = ReplyKeyboardRemove()
