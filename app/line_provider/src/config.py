import logging
from contextlib import suppress

from pydantic import BaseSettings, Field, AnyHttpUrl

with suppress(ImportError):
    # подгрузка переменных для локальной разработки, вне докер-контейнера
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='ci/.env')

logging.basicConfig(level=logging.INFO, format='%(message)s')


class Settings(BaseSettings):
    BET_MAKER_URL: AnyHttpUrl = Field(...)
    BET_MAKER_EXPORT_AUTH: str = Field(...)


settings = Settings()
