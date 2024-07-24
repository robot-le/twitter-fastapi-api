from src.utils import create_response
from src.models import User
from src.schemas import User as UserSchema, ResponseBaseWithObject, ResponseBase, UserUpdate
from src.dependencies import CurrentUserDep, SessionDep

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from sqlmodel import select, or_

router = APIRouter(prefix='/me')


@router.get("", response_model=ResponseBaseWithObject[UserSchema])
async def get_current_user(
        current_user: CurrentUserDep,
) -> JSONResponse:
    return create_response(
        'Current User',
        obj=UserSchema(**current_user.model_dump()),
        status_code=status.HTTP_200_OK,
    )


@router.patch("", response_model=ResponseBaseWithObject[UserSchema])
async def update_current_user(
        current_user: CurrentUserDep,
        session: SessionDep,
        changes: UserUpdate,
):
    print()

    statement = select(User).where(or_(
        User.username == changes.username,
        User.email == changes.email,
        ))
    existing_user = await session.scalar(statement)
    error = None
    if existing_user:
        if existing_user.email == changes.email and existing_user.username == changes.username:
            error = 'Username and email is taken'
        elif existing_user.username == changes.username and existing_user.email != changes.email:
            error = 'Username is taken'
        elif existing_user.email == changes.email and existing_user.username != changes.username:
            error = 'Email is taken'

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    update_data = changes.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(update_data)
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return create_response(
        message='User updated successfully',
        obj=UserSchema(**current_user.model_dump())
    )


@router.delete("", response_model=ResponseBase)
async def delete_current_user(
        current_user: CurrentUserDep,
        session: SessionDep,
):
    await session.delete(current_user)
    await session.commit()
    return create_response(
        'User deleted successfully',
    )
