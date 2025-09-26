from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product

async def orm_add_product(session: AsyncSession, data: dict):
    product = Product(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"]
    )

    session.add(product)
    await session.commit()
