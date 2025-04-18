import jwt
from enum import IntEnum
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from app.config import settings
from app.schemas.token import Token
from app.config import get_db
from app.models.user import User

auth_bearer = HTTPBearer()


class Role(IntEnum):
    USER = 0
    LIBRARIAN = 1
    ADMIN = 2


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


def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(auth_bearer),
    db=Depends(get_db),
):
    token = auth.credentials
    user_id = int(decode_jwt_token(token)["sub"])
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=401, detail="Token pointing to non-existent user"
        )
    return user


def get_current_user_with_minimum_role(required_role: Role):
    def dependency(
        user: User = Depends(get_current_user),
    ):
        if user.access_level < required_role:
            raise HTTPException(status_code=403, detail="Insufficient rights")
        return user

    return dependency
