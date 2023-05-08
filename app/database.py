from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Settings

settings = Settings(
    DATABASE_PORT=5432,
    POSTGRES_PASSWORD="password123",
    POSTGRES_USER="postgres",
    POSTGRES_DB="backend_db",
    POSTGRES_HOST="postgres",
    POSTGRES_HOSTNAME="127.0.0.1",
)

POSTGRES_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(POSTGRES_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
