from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegraph_access_token: str = ""
    devto_api_key: str = ""
    github_token: str = ""
    bluesky_handle: str = ""
    bluesky_app_password: str = ""
    request_timeout: float = 15.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
