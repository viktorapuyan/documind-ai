
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from app.db.base import Base
import app.models  # Registers both ORM models


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TestSettings(BaseSettings):
    test_database_url: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )


settings = TestSettings()

if settings.test_database_url.rsplit("/", 1)[-1] != "documind_test_db":
    raise ValueError("Refusing to initialize a non-test database")

engine = create_engine(settings.test_database_url)

Base.metadata.create_all(bind=engine)

print("Test database tables created successfully.")
