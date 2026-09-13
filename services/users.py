from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from models.users import UsersModel


async def get_user_by_email(email: str, session: AsyncSession) -> UsersModel | None:
    """
    Get User by email from database.
    
    :email: User email.

    :retun: User or None
    """
    return await get_user_by_field(UsersModel.email, email, session)


async def get_user_by_id(user_id: str, session: AsyncSession) -> UsersModel | None:
    """
    Get User by id from database.
    
    :user_id: User id.

    :retun: User or None
    """
    return await get_user_by_field(UsersModel.id, user_id, session)


async def get_user_by_field(
        filter_field: InstrumentedAttribute[Any], 
        search_value: Any, 
        session: AsyncSession,
) -> UsersModel | None:
    """
    Get User by field from database.
    
    :filter_field: Fields to search in.
    :search_value: Search terms.

    :retun: User or None
    """
    if search_value is None:
        return None

    query = select(UsersModel).where(filter_field == search_value)
    return await session.scalar(query)

