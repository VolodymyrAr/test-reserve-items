from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "very-secret"
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "postgres"


env = Settings()
