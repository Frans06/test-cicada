import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    READER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"
    READER_DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://root:fastapi@localhost:3306/fastapi"
    READER_DB_URL: str = f"mysql+aiomysql://root:fastapi@localhost:3306/fastapi"


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"
    READER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"


class TestConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://root:fastapi@localhost:3306/test"
    READER_DB_URL: str = f"mysql+aiomysql://root:fastapi@localhost:3306/test"
    TEST_DB_URL: str = f"mysql+pymysql://root:fastapi@localhost:3306/test"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


def get_config(env: str = "local"):
    env = os.getenv("ENV", env)
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config: Config = get_config()
