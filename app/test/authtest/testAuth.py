from app.auth.authService import (
    verifyPassword, authenticateAdmin,
    createAccessToken
)

def test_Verify_password(testAdmin):
    assert verifyPassword('secret123', testAdmin.passwordHash) is True
    
def test_Verify_passwordWrong(testAdmin):
    assert verifyPassword("wrongpassword", testAdmin.passwordHash) is False
    
def test_Authenticate_Admin_success(dbSession, testAdmin):
    admin = authenticateAdmin(dbSession, "admin_test", "secret123")
    assert admin is not None
    assert admin.usename == "admin_test"

def test_Authenticate_Adminwrong_Password(dbSession):
    admin = authenticateAdmin(dbSession, "admin_test", "wrongpass")
    assert admin is not True
    assert admin.usename == "admin_test"
    
def test_Authenticate_Admin_None_exist(dbSession):
    admin = authenticateAdmin(dbSession, "nonexistent", "secret123")
    assert admin is None
    
def test_Create_Access_Token(testAdmin):
    data = {"sub": testAdmin.username}
    token = createAccessToken(data)
    assert isinstance(token, str)
    assert len(token) > 0