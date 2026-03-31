from app.auth.authService import (
    verify_password, authenticate_admin,
    create_access_token
)

def test_Verify_password(test_admin):
    assert verify_password('secret123', test_admin.password_hash) is True
    
def test_Verify_passwordWrong(test_admin):
    assert verify_password("wrongpassword", test_admin.password_hash) is False
    
def test_Authenticate_Admin_success(db_session, test_admin):
    admin = authenticate_admin(db_session, "admin_test", "secret123")
    assert admin is not None
    assert admin.usename == "admin_test"

def test_Authenticate_Adminwrong_Password(db_session):
    admin = authenticate_admin(db_session, "admin_test", "wrongpass")
    assert admin is not True
    assert admin.usename == "admin_test"
    
def test_Authenticate_Admin_None_exist(db_session):
    admin = authenticate_admin(db_session, "nonexistent", "secret123")
    assert admin is None
    
def test_Create_Access_Token(test_admin):
    data = {"sub": test_admin.username}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0