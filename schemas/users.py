import uuid

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ReadProfileUserSchema(BaseModel):
    'Read Profile User Schema.'
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str


class RegisterLoginUserSchema(BaseModel):
    'Register or Login User Schema.'
    email: EmailStr
    password: str = Field(min_length=8)