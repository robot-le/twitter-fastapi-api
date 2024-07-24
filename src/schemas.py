from sqlmodel import Field, SQLModel
from pydantic import EmailStr, model_validator, BaseModel
from typing import Generic, TypeVar, Literal, Self
from src.config import settings

T = TypeVar('T')


class ResponseBase(BaseModel):
    status: Literal['success', 'error']
    status: str
    message: str


class ResponseBaseWithObject(ResponseBase, Generic[T]):
    obj: T


class UserBase(SQLModel):
    id: int | None = None
    username: str = Field(max_length=32)
    email: EmailStr | None = None


class User(UserBase):
    pass


class UserLogin(UserBase):
    password: str


class UserInput(UserLogin):
    password2: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self


class UserUpdate(SQLModel):
    username: str | None = None
    bio: str | None = None
    email: str | None = None


class Token(SQLModel):
    access_token: str
    token_type: str = 'Bearer'
    expires_in: int
    user: User


class PostCreate(SQLModel):
    body: str = Field(max_length=settings.post_char_limit)
