from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

DATABASE_URL = "sqlite:///omniscience.db"

# The connect_args is needed for SQLite to allow multi-threaded access, which is common in web applications.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal will be the session factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Creates all the tables in the database.
    This function should be called once when the application starts.
    """
    Base.metadata.create_all(bind=engine)
