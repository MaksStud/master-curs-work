from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    project_name: str = 'Test'
    port: int = 8000
    debug: bool = False




settings = _Settings()
