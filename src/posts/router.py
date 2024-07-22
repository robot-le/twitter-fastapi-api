from src.models import Post, PostCreate
from src.schemas import ResponseBase
from src.dependencies import CurrentUserDep, SessionDep, AuthDep

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from starlette.requests import Request

from sqlmodel import select


router = APIRouter(prefix='/posts')


@router.post('/')
async def create_post(
        post: PostCreate,
        request: Request,
        session: SessionDep,
        current_user: CurrentUserDep,
):
    p = Post(
        body=post.body,
        author=current_user,
    )
    session.add(p)
    await session.commit()
    await session.refresh(p)
    return JSONResponse(
        jsonable_encoder(ResponseBase[Post](
            status='success',
            message='Post created successfully',
            data=Post(**p.model_dump()),
        )),
        status_code=status.HTTP_201_CREATED,
        headers={
            'Location': f'{request.base_url}posts/{p.id}'
        }
    )


@router.get('/{post_id}')
async def get_post(
        post_id: int,
        session: SessionDep,
        token: AuthDep,
) -> Post:
    query = select(Post).where(Post.id == post_id)
    p = await session.scalar(query)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
    return p


@router.delete('/{post_id}', status_code=200)
async def delete_post(
        post_id: int,
        session: SessionDep,
        token: AuthDep,
):
    p = await session.get(Post, post_id)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
    await session.delete(p)
    await session.commit()
    return ResponseBase(
        status='success',
        message='Post deleted successfully',
    )
