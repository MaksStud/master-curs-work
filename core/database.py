from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


engine = create_async_engine(settings.db_url)
session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    ...

async def get_db():
    """Get database."""
    async with session() as db:
        yield db


SessionDep = Annotated[AsyncSession, Depends(get_db)]