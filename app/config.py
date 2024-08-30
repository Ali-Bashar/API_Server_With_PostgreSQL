from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str 
    database_host: str 
    database_username: str 
    database_port: str 
    database_password : str
    database_name : str 
    algorithm : str 
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"

settings = Settings()

