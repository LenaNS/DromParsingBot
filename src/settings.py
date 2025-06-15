from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="src/.env", env_file_encoding="utf-8", extra="ignore"
    )

    url: str = "https://httpbin.org/post"
    token: SecretStr

    @classmethod
    def load(cls) -> "Settings":
        return cls()
