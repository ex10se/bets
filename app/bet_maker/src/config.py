from contextlib import suppress

from pydantic import BaseSettings, PostgresDsn, validator

with suppress(ImportError):
    # подгрузка переменных для локальной разработки, вне докер-контейнера
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='ci/.env')


class Settings(BaseSettings):
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'postgres'

    BET_MAKER_EXPORT_AUTH: str = 'auth'

    DSN_DATABASE_ASYNC: PostgresDsn = None

    @validator('DSN_DATABASE_ASYNC', pre=True, always=True)
    def prepare_dsn(cls, _, values: dict) -> str:
        return (
            f'postgresql+asyncpg://{values["POSTGRES_USER"]}:{values["POSTGRES_PASSWORD"]}'
            f'@psql/{values["POSTGRES_DB"]}'
        )


settings = Settings()
