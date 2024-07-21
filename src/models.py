import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from pydantic import EmailStr
from sqlalchemy import text


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # id: int | None = Field(default=None, primary_key=True)
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
    # password_hash: str
    # post_id: int = Field(foreign_key='post.id')
    posts: list['Post'] | None = Relationship(back_populates='author')
    bio: str | None = Field(max_length=140)


class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # id: int | None = Field(default=None, primary_key=True)
    body: str = Field(max_length=140)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("TIMEZONE('utc', now())"),
        )
    )
    user_id: uuid.UUID = Field(foreign_key='user.id')
    author: 'User' = Relationship(back_populates='posts')
