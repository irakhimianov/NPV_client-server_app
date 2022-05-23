from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080


settings = Settings(_env_file="../.env",
                    _env_file_encoding="utf-8")