from sql.database import Base, engine
import asyncio


async def create_db():
    """
    Cоздание таблиц базы данных
    """
    async with engine.begin() as conn:
        from sql.models import  Products
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


asyncio.run(create_db())
