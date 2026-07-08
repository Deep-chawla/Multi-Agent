from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings

from app.database.base import Base


engine = create_engine(
    Settings.DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()