from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# Пример секрета и алгоритма (их нужно взять из вашего backend-конфигуратора)
SECRET_KEY = "YourSuperSecureSecretKeyThatIsVeryLong"
ALGORITHM = "HS256"

# Определяем схему для Bearer-токена
auth_scheme = HTTPBearer()

def decode_jwt(token: str) -> dict:
    """
    Расшифровка и проверка JWT-токена.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict:
    """
    Зависимость для извлечения и проверки текущего пользователя из токена.
    """
    return decode_jwt(credentials.credentials)
