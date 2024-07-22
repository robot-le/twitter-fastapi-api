from datetime import datetime
from sqlalchemy import text
from typing import Self
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from pydantic import EmailStr, model_validator


class Post(SQLModel, table=True):
    __tablename__ = 'posts'

    id: int | None = Field(default=None, primary_key=True)
    body: str = Field(max_length=140)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('utc', now())"),
        )
    )
    user_id: int = Field(foreign_key='users.id', ondelete='CASCADE')
    author: 'User' = Relationship(back_populates='posts')


class UserInput(SQLModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(
        max_length=32,
        index=True,
        unique=True,
    )
    email: EmailStr = Field(
        max_length=120,
        index=True,
        unique=True,
    )
    password: str  # todo: add validators to the password field
    posts: list['Post'] | None = Relationship(back_populates='author')
    bio: str | None = Field(max_length=140)


class UserCreated(SQLModel):
    id: int
    username: str
    email: str


class UserLogin(SQLModel):
    username: str = Field(
        max_length=32,
        index=True,
        unique=True,
    )
    password: str
