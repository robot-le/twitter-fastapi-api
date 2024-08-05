from sqlmodel import (
    Field,
    SQLModel,
    Relationship,
    Column,
    DateTime,
)
from datetime import datetime
from pydantic import EmailStr
from src.config import settings
from sqlmodel import text, select, and_
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
# from sqlalchemy.ext.hybrid import hybrid_property
# from database import get_session
# from sqlalchemy.orm import Session
# from pydantic import computed_field


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


class Followers(SQLModel, table=True):
    __tablename__ = 'followers'

    follower_id: int | None = Field(default=None, foreign_key='users.id', primary_key=True)
    followed_id: int | None = Field(default=None, foreign_key='users.id', primary_key=True)


class User(SQLModel, AsyncAttrs, table=True):
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

    following: list['User'] = Relationship(
        back_populates='followers',
        link_model=Followers,
        sa_relationship_kwargs={
            'primaryjoin': 'User.id == Followers.follower_id',
            'secondaryjoin': 'User.id == Followers.followed_id',
        }
    )

    followers: list['User'] = Relationship(
        back_populates='following',
        link_model=Followers,
        sa_relationship_kwargs={
            'primaryjoin': 'User.id == Followers.followed_id',
            'secondaryjoin': 'User.id == Followers.follower_id',
        }
    )

    async def get_follow_rel(self, user, session):
        query = select(Followers).where(and_(
            Followers.follower_id == self.id,
            Followers.followed_id == user.id,
            ))
        return await session.scalar(query)

    async def follow(self, user, session):
        if await self.get_follow_rel(user, session) is None:
            following = await self.awaitable_attrs.following
            following.append(user)

    async def unfollow(self, user, session):
        if follow_rel := await self.get_follow_rel(user, session):
            await session.delete(follow_rel)

    async def followers_count(self, user):
        pass
