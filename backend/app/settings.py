from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://asm3:password@localhost:5432/asm3_db"
    duckdb_url: str = "duckdb:///data/duck.db"
    scylla_url: str = "localhost"

settings = Settings()