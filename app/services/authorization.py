import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from app.config import settings
from ..schemas.token import Token


auth_bearer = HTTPBearer()


def create_jwt_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.JWT_TOKEN_EXPIRATION),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return Token(access_token=token, token_type="Bearer")


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user_id(auth: str = Depends(auth_bearer)):
    token = auth.credentials
    return int(decode_jwt_token(token)["sub"])
