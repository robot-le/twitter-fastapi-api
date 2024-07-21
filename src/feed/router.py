from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.database import get_session
from src.models import Post, User

router = APIRouter()


@router.post('/')
def root(*, session: Session = Depends(get_session),
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
    session.commit()
    session.refresh(db_post)
    return db_post
