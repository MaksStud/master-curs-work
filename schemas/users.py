import uuid

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserEmailSchema(BaseModel):
    email: EmailStr


class ReadProfileUserSchema(UserEmailSchema):
    """Read Profile User Schema."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


class RegisterLoginUserSchema(UserEmailSchema):
    """Register or Login User Schema."""
    password: str = Field(min_length=8)


class ConfirmEmailSchema(UserEmailSchema):
    """Confirm Email Schema."""
    otp_code: int = Field(ge=1000, le=9999)
