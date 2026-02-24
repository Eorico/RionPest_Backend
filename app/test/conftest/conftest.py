from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Database.database import Base, getDb
from app.main import app
from app.Controllers.inventory.inventoryController import InventoryController
import pytest

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:RAIONN123@localhost/pest_inventory"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True,
    pool_pre_ping=True
    )
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

@pytest.fixture(scope="function")
def db_Session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        
@pytest.fixture(scope="function")
def client(dbSession):
    def overrideGetDb():
        return dbSession
    app.dependency_overrides[getDb] = overrideGetDb
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    
@pytest.fixture(scope="function")
def controller(dbSession):
    yield InventoryController(dbSession)    