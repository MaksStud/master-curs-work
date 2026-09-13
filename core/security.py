from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

from models.users import UsersModel
from core.database import SessionDep
from services.jwt_tokens import decode_token
from services.users import get_user_by_id

security = HTTPBearer()


def _extract_user_id_from_token(payload: dict) -> str:
    """Extract and validate user_id from token payload."""
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return user_id


def _validate_token(credentials: HTTPAuthCredentials) -> dict:
    """Decode and validate access token."""
    payload = decode_token(credentials.credentials, expected_type="access")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


async def get_current_user(
    credentials: Annotated[HTTPAuthCredentials, Depends(security)],
    session: SessionDep,
) -> UsersModel:
    """Get authenticated user from token and database."""
    payload = _validate_token(credentials)
    user_id = _extract_user_id_from_token(payload)
    user = await get_user_by_id(user_id, session)
    return user


CurrentUser = Annotated[str, Depends(get_current_user)]
