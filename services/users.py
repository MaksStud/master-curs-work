from typing import Any

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from models.users import UsersModel

from core.constantes import USER_ALREDY_EXIST


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

async def ensure_no_active_user_by_email(email: str, session: AsyncSession) -> UsersModel | None:
    """
    Validate that no active user is registered with the given email.

    :email: User email.
    :session: Database session.

    :raises HTTPException: If an active user with this email already exists.

    :retun: Existing inactive user or None.
    """
    exist_user = await get_user_by_email(email, session)

    if exist_user and exist_user.is_active:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail=USER_ALREDY_EXIST
             )

    return exist_user