from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "YourSuperSecureSecretKeyThatIsVeryLong"
ALGORITHM = "HS256"

# Bearer-token
auth_scheme = HTTPBearer()

# Check token
def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

# return token-info 
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    return decode_jwt(credentials.credentials)
