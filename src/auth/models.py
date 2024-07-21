from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr


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
    # password_hash: str
    posts: list['Post'] | None = Relationship(back_populates='author')
    bio: str | None = Field(max_length=140)
