from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="О магазине"),
        ],
        [
            KeyboardButton(text="Варианты доставки"),
            KeyboardButton(text="Варианты оплаты"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

del_keyboard = ReplyKeyboardRemove()

start_keyboard_with_builder_1 = ReplyKeyboardBuilder()
start_keyboard_with_builder_1.add(
    KeyboardButton(text="Меню"),
    KeyboardButton(text="О магазине"),
    KeyboardButton(text="Варианты доставки"),
    KeyboardButton(text="Варианты оплаты"),
)
start_keyboard_with_builder_1.adjust(2, 2)

start_keyboard_with_builder_2 = ReplyKeyboardBuilder()

# создание клавиатуры на основе другой
start_keyboard_with_builder_2.attach(start_keyboard_with_builder_1)

# добавить кнопку в новый ряд
start_keyboard_with_builder_2.row(KeyboardButton(text="Оставить отзыв"))

test_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать опрос", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="Отправить номер 📞", request_contact=True),
            KeyboardButton(text="Отправить локацию 🗺️", request_location=True)
        ],
    ],
    resize_keyboard=True
)
