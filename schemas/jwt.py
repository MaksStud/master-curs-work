from pydantic import BaseModel, Field


class JWTTokensSchema(BaseModel):
    """JWT Tokens Schema."""
    refresh_token: str
    access_token: str
    token_type: str = 'bearer'


class RefreshTokenSchema(BaseModel):
    """Refresh Token Schema."""
    refresh_token: str


class AccessTokenSchema(BaseModel):
    """Access Token Schema."""
    access_token: str
    token_type: str = 'bearer'