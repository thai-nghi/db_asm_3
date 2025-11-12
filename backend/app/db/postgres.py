from app.settings import settings
from app.db import models
from sqlmodel import create_engine, SQLModel, Session, text
from pathlib import Path

engine = create_engine(settings.database_url, echo=True)

def init_database():
    """Initialize DuckDB database by executing the duck_init.sql script only if tables don't exist."""
    
    # Check if the user table already exists
    with Session(engine) as session:
        try:
            # Try to check if the user table exists using DuckDB's information_schema
            result = session.exec(text("SELECT table_name FROM information_schema.tables WHERE table_name = 'user'"))
            table_exists = result.fetchone() is not None
            
            if table_exists:
                print("Posstgres database already initialized (user table exists)")
                return
                
        except Exception:
            # If the query fails, assume tables don't exist and proceed with initialization
            print("DuckDB database not initialized, proceeding with setup")
    
    # Get the path to the seed_data.sql file
    current_dir = Path(__file__).parent
    sql_file_path = current_dir / "seed/seed_data.sql"


    SQLModel.metadata.create_all(engine)

    if not sql_file_path.exists():
        raise FileNotFoundError(f"SQL initialization file not found: {sql_file_path}")

    print("Initializing Postgres database...")
    
    # Read and execute the SQL file
    with open(sql_file_path, 'r') as file:
        sql_content = file.read()
    
    with Session(engine) as session:
        session.exec(text(sql_content))
        session.commit()

    print("Postgres database initialization completed")

# Initialize the database when the module is imported
init_database()
