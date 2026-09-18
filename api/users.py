from fastapi import APIRouter, HTTPException, status

from core.database import SessionDep
from core.constantes import (
    EMAIL_OR_PASSWORD_IS_NOT_VALID,
    USER_ALREDY_EXIST,
    OTP_USER_MASSAGE,
    OTP_SUBJECT
    )
from core.security import CurrentUser

from models.users import UsersModel

from schemas.users import RegisterLoginUserSchema, ReadProfileUserSchema
from schemas.jwt import JWTTokensSchema

from services.hash_password import hash_password, is_valid_password
from services.users import get_user_by_email
from services.jwt_tokens import create_token_pair
from services.otp_code import OTPCodeDep

from tasks.send_message import send_massage


router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register')
async def register(user: RegisterLoginUserSchema, session: SessionDep, otp_service: OTPCodeDep) -> ReadProfileUserSchema:
    """
    Register user.
    If user not alredy exist in database, save and return his profile.
    """
    exist_user = await get_user_by_email(user.email, session)

    if exist_user and exist_user.is_active:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail=USER_ALREDY_EXIST
             )
    elif not exist_user:
        new_user = UsersModel(
            email=user.email,
            password=hash_password(user.password)
        )

        session.add(new_user)
        await session.commit()
    else:
        new_user = exist_user

    otp_code = await otp_service.generate_code()

    email = new_user.email
    massage = OTP_USER_MASSAGE.format(otp_code=otp_code)
    await otp_service.set_code(email, str(otp_code))

    send_massage.delay('email', [email], massage, OTP_SUBJECT)

    return new_user


@router.post('/login')
async def login(user: RegisterLoginUserSchema, session: SessionDep) -> JWTTokensSchema:
    """
    Login user.
    If user email and password valid return JWT token.
    """
    exist_user: UsersModel = await get_user_by_email(user.email, session)

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




    
@router.get('/profile')
def get_user_profile(user: CurrentUser) -> ReadProfileUserSchema:
    return user