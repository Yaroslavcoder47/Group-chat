from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    host: str = "localhost"
    port: str = "5432"
    user: str
    password: str
    db_name: str
    conn_str: str
    

settings = Settings()