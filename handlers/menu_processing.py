from aiogram.types import InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_banner, orm_get_categories
from keyboards.inline import get_user_main_btns, get_user_catalog_btns


async def main_menu(session: AsyncSession, level: int, menu_name: str):
    banner = await orm_get_banner(session, menu_name)

    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    keyboard = get_user_main_btns(level=level)

    return image, keyboard


async def catalog(session: AsyncSession, level: int, menu_name: str):
    banner = await orm_get_banner(session, menu_name)

    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    categories = await orm_get_categories(session=session)

    keyboard = get_user_catalog_btns(level=level, categories=categories)

    return image, keyboard


async def get_menu_content(session: AsyncSession, level: int, menu_name: str):
    if level == 0:
        return await main_menu(session, level, menu_name)
    elif level == 1:
        return await catalog(session, level, menu_name)