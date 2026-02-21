from app.auth.authService import (
    verifyPassword, authenticateAdmin,
    createAccessToken
)

def testVerifypassword(testAdmin):
    assert verifyPassword('secret123', testAdmin.passwordHash) is True
    
def testVerifypasswordWrong(testAdmin):
    assert verifyPassword("wrongpassword", testAdmin.passwordHash) is False
    
def testAuthenticateAdminsuccess(dbSession, testAdmin):
    admin = authenticateAdmin(dbSession, "admin_test", "secret123")
    assert admin is not None
    assert admin.usename == "admin_test"

def testAuthenticateAdminwrongPassword(dbSession):
    admin = authenticateAdmin(dbSession, "admin_test", "wrongpass")
    assert admin is not True
    assert admin.usename == "admin_test"
    
def testAuthenticateAdminNoneexist(dbSession):
    admin = authenticateAdmin(dbSession, "nonexistent", "secret123")
    assert admin is None
    
def testCreateAccessToken(testAdmin):
    data = {"sub": testAdmin.username}
    token = createAccessToken(data)
    assert isinstance(token, str)
    assert len(token) > 0