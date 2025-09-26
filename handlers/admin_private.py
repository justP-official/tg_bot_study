from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin

from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard

from database.orm_query import orm_add_product, orm_delete_product, orm_get_product, orm_get_products, orm_update_product


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    await message.answer("ОК, вот список товаров")

    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
                reply_markup=get_callback_btns(btns={
                    "Удалить": f"delete_{product.id}",
                    "Изменить": f"change_{product.id}"
                })
        )


#Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }


@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )

    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter("*"), Command("отмена"))  # любое состояние
@admin_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return
    
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предыдущего шага нет. Или введите название товара, или напишите "отмена"')
        return
    
    previous_state = None

    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_state)
            await message.answer(f"ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous_state.state]}")
            return
        
        previous_state = step


@admin_router.message(StateFilter(AddProduct.name), F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Введите описание товара")

    await state.set_state(AddProduct.description)


@admin_router.message(StateFilter(AddProduct.name))
async def process_wrong_name(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные. Введите название товара")


@admin_router.message(StateFilter(AddProduct.description), F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer("Введите стоимость товара")

    await state.set_state(AddProduct.price)


@admin_router.message(StateFilter(AddProduct.description))
async def process_wrong_description(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные. Введите описание товара")


@admin_router.message(StateFilter(AddProduct.price), F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)

    await message.answer("Загрузите изображение товара")

    await state.set_state(AddProduct.image)


@admin_router.message(StateFilter(AddProduct.price))
async def process_wrong_price(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные. Введите цену товара")


@admin_router.message(StateFilter(AddProduct.image), F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)

    data = await state.get_data()

    try:
        await orm_add_product(session=session, data=data)
        await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    except Exception as e:
        await message.answer(
            f"Ошибка: {e}",
            reply_markup=ADMIN_KB
        )
    finally:
        await state.clear()


@admin_router.message(StateFilter(AddProduct.image))
async def process_wrong_image(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные. Загрузите изображение товара")
