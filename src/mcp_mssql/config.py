from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MSSQL_SERVER: str = Field(default="localhost")
    MSSQL_DATABASE: str = Field(default="master")
    MSSQL_USERNAME: str = Field(default="sa")
    MSSQL_PASSWORD: str = Field(default="your_password")
    MSSQL_PORT: int = Field(default=1433)
    MSSQL_DRIVER: str = Field(default="ODBC Driver 18 for SQL Server")
    MSSQL_ENCRYPT: bool = Field(default=True)
    MSSQL_TRUST_SERVER_CERT: bool = Field(default=False)

    POOL_SIZE: int = Field(default=10)
    POOL_MAX_OVERFLOW: int = Field(default=20)
    POOL_TIMEOUT: int = Field(default=30)
    POOL_RECYCLE: int = Field(default=3600)

    MAX_ROWS: int = Field(default=10000)
    QUERY_TIMEOUT: int = Field(default=120)
    ALLOW_WRITE_OPERATIONS: bool = Field(default=False)
    ALLOWED_SCHEMAS: List[str] = Field(default=["dbo"])

    REDIS_URL: str = Field(default="redis://localhost:6379")
    REDIS_ENABLED: bool = Field(default=False)
    SCHEMA_CACHE_TTL: int = Field(default=3600)

    LOG_LEVEL: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()