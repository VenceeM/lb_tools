from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_HOST:str
    PASSWORD_SECRET:str
    JWT_SECRET:str
    JWT_ALORITHM:str
    REDIS_HOST:str
    REDIS_PORT:str
    SMTP_SERVER:str
    SMTP_PORT:str
    SENDER_EMAIL:str
    SENDER_PASSWORD:str
    OTHER_DB_URL:str
    OTHER_HOST:str
    OTHER_PORT:str
    OTHER_USER:str
    OTHER_PASSWORD:str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )
    
Config = Settings()