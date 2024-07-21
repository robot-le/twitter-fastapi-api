from src.models import Post, User
from src.database import get_session
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter()


@router.post('/')
async def root(*, session: AsyncSession = Depends(get_session),
               # post: Post
               ):
    author = User(
        username='user1',
        email='user1@mail.com',
    )
    db_post = Post(
        body='hello',
        author=author,
    )
    session.add(author)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post
