from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from datetime import datetime
from pydantic import EmailStr
from src.config import settings
from sqlmodel import text


class Post(SQLModel, table=True):
    __tablename__ = 'posts'

    id: int | None = Field(default=None, primary_key=True)
    body: str = Field(max_length=settings.post_char_limit)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('utc', now())"),
        )
    )
    user_id: int = Field(foreign_key='users.id', ondelete='CASCADE')
    author: 'User' = Relationship(back_populates='posts')


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
    posts: list['Post'] | None = Relationship(back_populates='author', cascade_delete=True)
    bio: str | None = Field(max_length=140)

