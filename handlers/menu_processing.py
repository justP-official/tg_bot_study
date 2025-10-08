from aiogram.types import InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_banner, orm_get_categories, orm_get_products, Paginator
from keyboards.inline import get_user_main_btns, get_user_catalog_btns, get_products_btns


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


def pages(paginator: Paginator):
    btns = dict()

    if paginator.has_previous():
        btns["◀️ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶️"] = "next"

    return btns


async def products(
    session: AsyncSession, 
    level: int, 
    category: int,
    page: int
):
    products_list = await orm_get_products(session=session, category_id=category)

    paginator = Paginator(products_list, page=page)
    product = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=product.image,
        caption=f"<strong>{product.name}\
            </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}\n\
            <strong>Товар {paginator.page} из {paginator.pages}</strong>"
    )

    pagination_btns = pages(paginator)

    keyboards = get_products_btns(
        level=level,
        category=category,
        page=page,
        pagination_btns=pagination_btns,
        product_id=product.id,
    )

    return image, keyboards


async def get_menu_content(
    session: AsyncSession, 
    level: int, 
    menu_name: str,
    category: int | None = None,
    page: int | None = None
):
    if level == 0:
        return await main_menu(session, level, menu_name)
    elif level == 1:
        return await catalog(session, level, menu_name)
    elif level == 2:
        return await products(session, level, category, page)
    
