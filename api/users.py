from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from core.database import SessionDep
from core.constantes import (
    EMAIL_OR_PASSWORD_IS_NOT_VALID,
    OTP_USER_MASSAGE,
    OTP_SUBJECT,
    USER_IS_NOT_EXIST,
    OTP_CODE_IS_NOT_VALID,
    INVALID_TOKEN
    )
from core.security import CurrentUser

from models.users import UsersModel

from schemas.users import (
    RegisterLoginUserSchema,
    ReadProfileUserSchema,
    ConfirmEmailSchema
    )
from schemas.jwt import JWTTokensSchema, RefreshTokenSchema, AccessTokenSchema

from services.hash_password import hash_password, is_valid_password
from services.users import get_user_by_email, get_user_by_id, ensure_no_active_user_by_email
from services.jwt_tokens import create_token_pair, create_access_token, decode_token
from services.otp_code import OTPCodeDep

from tasks.send_message import send_massage


router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register')
async def register(user: RegisterLoginUserSchema, session: SessionDep, otp_service: OTPCodeDep) -> ReadProfileUserSchema:
    """
    Register user.
    If user not alredy exist in database, save and return his profile.
    """
    exist_user = await ensure_no_active_user_by_email(user.email, session)

    target_user = exist_user or UsersModel(
        email=user.email,
        password=hash_password(user.password)
    )

    if not exist_user:
        session.add(target_user)
        await session.commit()

    otp_code = await otp_service.generate_code()
    massage = OTP_USER_MASSAGE.format(otp_code=otp_code)

    await otp_service.set_code(target_user.email, str(otp_code))
    send_massage.delay('email', [target_user.email], massage, OTP_SUBJECT)

    return target_user


@router.post('/register/confirm')
async def register_confirm(data: ConfirmEmailSchema, session: SessionDep, otp_service: OTPCodeDep) -> Response:
    exist_user = await ensure_no_active_user_by_email(data.email, session)

    if exist_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USER_IS_NOT_EXIST
        )

    valid = await otp_service.validate_code(exist_user.email, data.otp_code)

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=OTP_CODE_IS_NOT_VALID
        )

    exist_user.is_active = True

    await session.commit()

    return Response()


@router.post('/login')
async def login(user: RegisterLoginUserSchema, session: SessionDep) -> JWTTokensSchema:
    """
    Login user.
    If user email and password valid return JWT token.
    """
    exist_user: UsersModel | None = await get_user_by_email(user.email, session)

    if exist_user is None or not exist_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EMAIL_OR_PASSWORD_IS_NOT_VALID
            )
    elif not is_valid_password(user.password, exist_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EMAIL_OR_PASSWORD_IS_NOT_VALID
            )

    jwt_tokens = create_token_pair(exist_user.id)
    return jwt_tokens


@router.post('/refresh')
async def refresh_tokens(data: RefreshTokenSchema, session: SessionDep) -> AccessTokenSchema:
    """
    Refresh access token.
    If refresh token valid and user exists, return new access token.
    """
    payload = decode_token(data.refresh_token, expected_type="refresh")

    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN)

    user = await get_user_by_id(payload.get("sub"), session)

    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN)

    return AccessTokenSchema(access_token=create_access_token(user.id))

@router.get('/profile')
def get_user_profile(user: CurrentUser) -> ReadProfileUserSchema:
    return user