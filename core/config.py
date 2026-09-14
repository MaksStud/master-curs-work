from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    project_name: str = 'Test'
    port: int = 8000
    debug: bool = False

    db_protocol: str = ''
    db_host: str = ''
    db_port: str = ''
    db_user: str = ''
    db_password: str = ''
    db_name: str = ''

    @property
    def db_url(self) -> str:
        return f"{self.db_protocol}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    redis_protocol: str = "redis"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def redis_url(self) -> str:
        return f"{self.redis_protocol}://{self.redis_host}:{self.redis_port}/{self.redis_db}"

settings = _Settings()
