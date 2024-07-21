import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from sqlalchemy import text


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
    user_id: int = Field(foreign_key='users.id')
    author: 'User' = Relationship(back_populates='posts')
