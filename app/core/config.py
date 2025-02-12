from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_HOST:str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
Config = Settings()