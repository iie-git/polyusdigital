import os
from typing import Any, Dict, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = 'store_app'
    POSTGRES_HOST: str = os.getenv('PG_SERVER_IP')
    POSTGRES_PORT: str = os.getenv('PG_SERVER_PORT')
    POSTGRES_USER: str = os.getenv('PG_SERVER_USER')
    POSTGRES_PASSWORD: str = os.getenv('PG_SERVER_PW')
    POSTGRES_DB: str = os.getenv('PG_SERVER_DB')
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        creds = {

            'user': values.data.get("POSTGRES_USER"),
            'pw': values.data.get("POSTGRES_PASSWORD"),
            'db': values.data.get('POSTGRES_DB'),
            'host': values.data.get("POSTGRES_HOST"),
            'port': values.data.get("POSTGRES_PORT"),
        }
        return 'postgresql+asyncpg://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % creds

    class Config:
        case_sensitive = True


settings = Settings()
