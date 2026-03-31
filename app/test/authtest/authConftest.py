from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Database.database import Base
from app.Models.admin.admin import Admin
from app.auth.authService import pwd_context
import pytest

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread" : False})
testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = testing_session_local()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture
def test_admin(db_session):
    password = "secret123"
    hash_password = pwd_context.hash(password)
    admin = Admin(username="admin_test", password_hash=hash_password)
    db_session.add(admin)
    db_session.commit()
    return admin