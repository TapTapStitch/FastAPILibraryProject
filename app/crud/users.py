from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from fastapi import HTTPException
from ..models.user import User
from ..schemas.user import SignUpSchema, SignInSchema, UpdateUserSchema
from .shared.db_utils import ensure_unique, fetch_by_id


class UsersCrud:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create(self, user_data: SignUpSchema):
        ensure_unique(self.db, User, "email", user_data.email, "Email already in use")
        user_params = user_data.model_dump()
        user_params["hashed_password"] = self._get_password_hash(
            user_params.pop("password")
        )
        user = User(**user_params)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, user_data: UpdateUserSchema):
        user = fetch_by_id(self.db, User, user_id, "User not found")
        user_params = user_data.model_dump(exclude_unset=True)
        if "email" in user_params and user_data.email != user.email:
            ensure_unique(
                self.db, User, "email", user_data.email, "Email already in use"
            )
        if "password" in user_params:
            user_params["hashed_password"] = self._get_password_hash(
                user_params.pop("password")
            )
        for key, value in user_params.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_data: SignInSchema):
        user = self.db.execute(
            select(User).where(User.email == user_data.email)
        ).scalar_one_or_none()
        if not user or not self._verify_password(
            user_data.password, user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    def _get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)
