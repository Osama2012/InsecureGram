from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "hardcoded_insecure_dev_key"
    DEBUG: bool = True
    ADMIN_API_KEY: str = "admin123"  # insecure static secret
    ENABLE_REMOTE_EXEC: bool = True
    INSECURE_UPLOAD_PATH: str = "/tmp"

settings = Settings()