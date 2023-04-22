from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

engine = create_async_engine(settings.DSN_DATABASE_ASYNC, echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        finally:
            await session.close()
