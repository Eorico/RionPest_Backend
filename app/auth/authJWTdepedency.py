from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.auth.authService import SECRET_KEY, ALGORITHM

oauthScheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def getCurrentAdmin(token: str = Depends(oauthScheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")