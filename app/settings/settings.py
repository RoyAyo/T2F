from pydantic_settings import BaseSettings
import os 

class Settings(BaseSettings):
    env:str = os.getenv("ENV","")
    PORT: str = os.getenv("PORT", "")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_file_path = os.getenv("ENV_FILE_PATH", ".env") 

# @lru_cache
def _get_settings():
    os_env = os.getenv("ENV", "DEV").upper()

    return Settings(env=os_env)

settings = _get_settings()