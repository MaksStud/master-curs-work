import random

from core.redis import RedisDep
from core.config import settings
from core.constantes import USER_OTP_REDIS_KEY


class OTPCodeService:
    """A service for managing OTP codes."""
    def __init__(self, _redis: RedisDep):
        self._redis = _redis
        self._live_time: int = settings.otp_live_time_second

    async def generate_code(self) -> int:
        """Generates an OTP code."""
        return random.randint(1000, 9999)

    async def set_code(self, user_identifier: str, code: str) -> int:
        """
        Set otp code for user.

        :user_identifier: A unique user field for user identification.
        :code: A code that will be stored for the user.

        :return: Returns the code received for all of them.
        """
        key = USER_OTP_REDIS_KEY.format(user_identifier=user_identifier)
        await self._redis.set(key, code, ex=self._live_time)

        return code

    async def get_code(self, user_identifier: str) -> int | None:
        """
        Get otp code for user.

        :user_identifier: A unique user field for user identification.

        :return: Returns a code from the Redis database.
        """
        key = USER_OTP_REDIS_KEY.format(user_identifier=user_identifier)
        code = await self._redis.get(key)
        return int(code) if code is not None else None
