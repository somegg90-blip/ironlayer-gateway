import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROVIDER: str = "openrouter"
    API_KEY: str = ""
    CUSTOM_SECRET_WORDS: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

    @property
    def base_url(self):
        if self.PROVIDER == "openrouter":
            return "https://openrouter.ai/api/v1"
        # Fallback just in case
        return "https://api.openai.com/v1"

    @property
    def headers(self):
        # OpenRouter requires these headers to identify the app
        return {
            "HTTP-Referer": "http://localhost:8000", 
            "X-Title": "IronLayer-Security-Gateway"
        }

    @property
    def secret_list(self):
        if not self.CUSTOM_SECRET_WORDS:
            return []
        return [word.strip() for word in self.CUSTOM_SECRET_WORDS.split(',') if word.strip()]

settings = Settings()