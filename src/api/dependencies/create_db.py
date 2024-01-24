from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from src.core.config import config

Base = declarative_base()
DATABASE_URL = config.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_db():
    await create_tables(engine)
