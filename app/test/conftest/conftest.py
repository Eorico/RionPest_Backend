from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Database.database import Base, getDb
from app.main import app
from app.Controllers.inventory.inventoryController import InventoryController
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite://:memory:"

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

def overrideGetdb():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[getDb]=overrideGetdb

Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
        
@pytest.fixture
def controller():
    db = TestingSessionLocal()
    Base.metadata.create_all(bind=engine)
    yield InventoryController(db)
    db.close()