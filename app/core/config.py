import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Configs(BaseSettings):
    # auth
    SECRET_KEY: str = os.getenv("MY_SECRET_KEY", "")

    # database
    DB: str = os.getenv("DB", "postgres")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", 5432)
    DB_ENGINE: str = "postgresql"

    DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"

    DATABASE_URI: str = DATABASE_URI_FORMAT.format(
        db_engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB
    )

    class Config:
        case_sensitive = True


configs = Configs()

