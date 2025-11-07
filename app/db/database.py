from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]        
DB_DIR  = APP_DIR / "db"                             
DB_DIR.mkdir(parents=True, exist_ok=True)             

DB_PATH = DB_DIR / "main.db"                          
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

