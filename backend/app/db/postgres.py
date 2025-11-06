from app.settings import settings
from app.db import models

from sqlmodel import create_engine, SQLModel

engine = create_engine(settings.database_url, echo=True)

SQLModel.metadata.create_all(engine)