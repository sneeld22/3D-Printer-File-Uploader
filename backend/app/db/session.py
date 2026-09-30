from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = make_url(settings.DATABASE_URL)
if DATABASE_URL.drivername == "postgresql":
    DATABASE_URL = DATABASE_URL.set(drivername="postgresql+psycopg2")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
