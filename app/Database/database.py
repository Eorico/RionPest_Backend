from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autcommit=False)

Base = declarative_base()

def getDb():
    db = SessionLocal()
    try: 
        yield db
    finally:  
        db.close()