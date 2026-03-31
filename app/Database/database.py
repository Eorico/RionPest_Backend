from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://RaionnPest:RAIONN123@localhost:3306/pest_inventory'
)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

session_local = sessionmaker(
    bind=engine, autoflush=False, 
    autcommit=False
)

Base = declarative_base()

def get_db():
    db = session_local()
    try: 
        yield db
    finally:  
        db.close()