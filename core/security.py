from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.users import UsersModel

from core.database import SessionDep
from core.constantes import INVALID_TOKEN

from services.jwt_tokens import decode_token, _extract_user_id_from_token
from services.users import get_user_by_id

security = HTTPBearer()
Credentials = Annotated[HTTPAuthorizationCredentials, Depends(security)]

async def get_current_user(credentials: Credentials, session: SessionDep ) -> UsersModel:
    """Get authenticated user from token and database."""
    payload = decode_token(credentials.credentials, expected_type="access")

    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN)    

    user_id = payload.get("sub", None)
    
    user = await get_user_by_id(user_id, session)
    return user


CurrentUser = Annotated[str, Depends(get_current_user)]
