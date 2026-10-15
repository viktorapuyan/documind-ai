
from pathlib import Path

import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestDatabaseSettings(BaseSettings):
    test_database_url: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )


@pytest.fixture
def db_session():
    settings = TestDatabaseSettings()

    if settings.test_database_url.rsplit("/", 1)[-1] != "documind_test_db":
        raise ValueError("Tests must use documind_test_db")

    engine = create_engine(settings.test_database_url)

    try:
        with engine.connect() as connection:
            transaction = connection.begin()

            try:
                with Session(
                    bind=connection,
                    join_transaction_mode="create_savepoint",
                ) as session:
                    yield session
            finally:
                transaction.rollback()
    finally:
        engine.dispose()
