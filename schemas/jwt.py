from pydantic import BaseModel, Field


class JWTTokensSchema(BaseModel):
    """JWT Tokens Schema."""
    refresh_token: str
    access_token: str
    token_type: str = 'bearer'