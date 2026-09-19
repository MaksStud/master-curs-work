from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from jwt.exceptions import InvalidTokenError

from core.config import settings


def create_token_pair(user_id: str) -> dict[str, str]:
    """
    Return dict with JWT tokens for User.
    
    :user_id: User id for which generation tokens.

    :return: Dict with refresh and access tokens and token type.
    """
    return {
        "refresh_token": _create_refresh_token(user_id),
        "access_token": create_access_token(user_id),
        "token_type": "bearer",
    }

def decode_token(token: str, expected_type: str) -> dict[str, Any] | None:
    """
    Decode and validate a JWT token.

    :token: Encoded JWT token.
    :expected_type: Expected token type ("access" or "refresh").

    :return: Token payload if the token is valid and of the expected type, None otherwise.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != expected_type:
            return None
        return payload
    except InvalidTokenError:
        return None

def create_access_token(user_id: str) -> str:
    """
    Create a new access token for the user.

    :user_id: User id for which the token is generated.

    :return: Encoded access JWT token.
    """
    return _create_jwt_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access",
    )


def _create_refresh_token(user_id: str) -> str:
    """
    Create a new refresh token for the user.

    :user_id: User id for which the token is generated.

    :return: Encoded refresh JWT token.
    """
    return _create_jwt_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type="refresh",
    )

def _create_jwt_token(data: dict[str, Any], expires_delta: timedelta, token_type: str) -> str:
    """
    Build and encode a JWT token with expiration and issued-at claims.

    :data: Base payload to encode into the token.
    :expires_delta: Token lifetime.
    :token_type: Token type stored in the "type" claim ("access" or "refresh").

    :return: Encoded JWT token.
    """
    payload = data.copy()
    now = datetime.now(timezone.utc)
    payload.update({
        "exp": now + expires_delta,
        "iat": now,
        "type": token_type,
    })
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
