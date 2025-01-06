from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime


class SignUpSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    model_config = ConfigDict(extra="forbid")


class UpdateUserSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    model_config = ConfigDict(extra="forbid")


class SignInSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(extra="forbid")
