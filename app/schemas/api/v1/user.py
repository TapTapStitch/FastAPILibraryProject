import re
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from datetime import datetime

PasswordPattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]*$"


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if len(value) > 100:
        raise ValueError("Password must be at most 100 characters long")
    if not re.match(PasswordPattern, value):
        raise ValueError(
            "Password must contain at least one uppercase letter, one lowercase letter and one digit"
        )
    return value


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str
    avatar_link: str
    access_level: int
    created_at: datetime
    updated_at: datetime


class SignUpSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    avatar_link: str

    model_config = ConfigDict(extra="forbid")

    @field_validator("password")
    def check_password(cls, value):
        return validate_password(value)


class UpdateUserSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    avatar_link: str | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("password")
    def check_password(cls, value):
        if value is None:
            return value
        return validate_password(value)


class SignInSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(extra="forbid")

    @field_validator("password")
    def check_password(cls, value):
        return validate_password(value)
