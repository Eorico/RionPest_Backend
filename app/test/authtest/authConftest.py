from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Database.database import Base
from app.Models.admin.admin import Admin
from app.auth.authService import pwdContext
import pytest

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread" : False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_Session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture
def test_Admin(dbSession):
    password = "secret123"
    hashPassword = pwdContext.hash(password)
    admin = Admin(username="admin_test", passwordHash=hashPassword)
    dbSession.add(admin)
    dbSession.commit()
    return admin