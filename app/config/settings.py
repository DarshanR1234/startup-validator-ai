from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    tavily_api_key: str

    development_model: str = "openai/gpt-oss-20b"
    advanced_model: str = "openai/gpt-oss-120b"

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()