from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    app_env: str = Field(default="local", alias="APP_ENV")
    app_name: str = Field(default="AI ScamShield", alias="APP_NAME")

    cors_origins: str = Field(default="http://localhost:5173", alias="CORS_ORIGINS")

    database_url: str = Field(
        default="postgresql+psycopg2://scamshield:scamshield@localhost:5432/scamshield",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    text_model_path: str = Field(default="ml/artifacts/text_model.joblib", alias="TEXT_MODEL_PATH")
    url_model_path: str = Field(default="ml/artifacts/url_model.joblib", alias="URL_MODEL_PATH")

    rdap_timeout_seconds: float = Field(default=2.5, alias="RDAP_TIMEOUT_SECONDS")

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

settings = Settings()
