from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Feishu
    feishu_app_id: str
    feishu_app_secret: str
    feishu_verification_token: Optional[str] = None
    feishu_event_encrypt_key: Optional[str] = None

    # GitLab
    gitlab_url: str = "https://gitlab.com"
    gitlab_private_token: str

    # General
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
