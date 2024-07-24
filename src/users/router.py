from fastapi import APIRouter, HTTPException, status

from src.utils import create_response
from src.models import User
from src.schemas import ResponseBase
from src.dependencies import CurrentUserDep, SessionDep


router = APIRouter(prefix='/users')


@router.post('/{user_id}/follow', response_model=ResponseBase)
async def follow(
        user_id: int,
        session: SessionDep,
        current_user: CurrentUserDep,
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User do not exists',
        )

    await current_user.follow(user, session)

    await session.commit()
    return create_response(
        message=f'You are following user {user.username}',
    )


@router.post('/{user_id}/unfollow', response_model=ResponseBase)
async def unfollow(
        user_id: int,
        session: SessionDep,
        current_user: CurrentUserDep,
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User do not exists',
        )

    await current_user.unfollow(user, session)
    await session.commit()
    return create_response(
        message=f'You are not following user {user.username}',
    )
