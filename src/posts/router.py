from src.utils import create_response
from src.models import Post
from src.schemas import PostCreate, ResponseBase, ResponseBaseWithObject
from src.dependencies import CurrentUserDep, SessionDep, AuthDep

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from starlette.requests import Request

from sqlmodel import select


router = APIRouter(prefix='/posts')


@router.post('', response_model=ResponseBaseWithObject[Post])
async def create_post(
        post: PostCreate,
        request: Request,
        session: SessionDep,
        current_user: CurrentUserDep,
) -> JSONResponse:
    p = Post(
        body=post.body,
        author=current_user,
    )
    session.add(p)
    await session.commit()
    await session.refresh(p)
    return create_response(
        'Post created successfully',
        obj=Post(**p.model_dump()),
        status_code=status.HTTP_201_CREATED,
        headers={
            'Location': f'{request.base_url}posts/{p.id}'
        }
    )


@router.get('/{post_id}', response_model=ResponseBaseWithObject[Post])
async def get_post(
        post_id: int,
        session: SessionDep,
        token_payload: AuthDep,
) -> JSONResponse:
    query = select(Post).where(Post.id == post_id)
    p = await session.scalar(query)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
    return create_response(
        message='Post',
        obj=Post(**p.model_dump())
    )


@router.delete(
    '/{post_id}',
    status_code=200,
    response_model=ResponseBase,
)
async def delete_post(
        post_id: int,
        session: SessionDep,
        token_payload: AuthDep,
) -> JSONResponse:
    p = await session.get(Post, post_id)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
    await session.delete(p)
    await session.commit()
    return create_response(
        message='Post deleted successfully',
    )
