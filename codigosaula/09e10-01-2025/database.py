from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:pgpass@localhost:5432/persistencia"
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
        db.commit()
    finally:
        db.close()