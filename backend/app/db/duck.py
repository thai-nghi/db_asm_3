from app.settings import settings
from app.db import models

from sqlmodel import create_engine, SQLModel, Session, text
import os
from pathlib import Path
from sqlalchemy.pool import NullPool

engine = create_engine(settings.duckdb_url, echo=True, poolclass=NullPool)

def init_database():
    """Initialize DuckDB database by executing the duck_init.sql script."""
    
    # Get the path to the duck_init.sql file
    current_dir = Path(__file__).parent.parent  # Go up to app directory
    sql_file_path = current_dir / "duck_init.sql"
    
    if not sql_file_path.exists():
        raise FileNotFoundError(f"SQL initialization file not found: {sql_file_path}")
    
    # Read and execute the SQL file
    with open(sql_file_path, 'r') as file:
        sql_content = file.read()
    
    with Session(engine) as session:
        session.exec(text(sql_content))
        session.commit()

# Initialize the database when the module is imported
init_database()