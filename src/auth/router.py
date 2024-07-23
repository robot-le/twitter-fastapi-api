from typing import Annotated
from datetime import timedelta
from sqlmodel import select, or_

from src.utils import create_response
from src.config import settings
from src.models import User
from src.schemas import UserInput, User as UserSchema, Token, ResponseBaseWithObject
from src.auth.auth import AuthHandler
from src.dependencies import SessionDep

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from starlette.requests import Request

router = APIRouter(prefix='/auth')
auth_handler = AuthHandler()


@router.post('/registration', response_model=ResponseBaseWithObject[UserSchema])
async def register(
        user: UserInput,
        session: SessionDep,
        request: Request,
) -> JSONResponse:
    statement = select(User).where(or_(
        User.username == user.username,
        User.email == user.email,
    ))
    existing_user = await session.scalar(statement)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username or email is taken',
        )

    hashed_pwd = auth_handler.hash_password(user.password)
    u = User(
        username=user.username,
        email=user.email,
        password=hashed_pwd,
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)

    return create_response(
        message='User successfully registered',
        obj=UserSchema(**u.model_dump()),
        status_code=status.HTTP_201_CREATED,
        headers={'Location': f'{request.base_url}users/{u.id}'},
    )


@router.post('/login', response_model=ResponseBaseWithObject[Token])
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep,
) -> JSONResponse:
    user_obj = await session.scalar(select(User).where(User.username == form_data.username))
    if not user_obj or not auth_handler.verify_password(user_obj.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires = timedelta(minutes=settings.token_expire_time_minutes)
    token = auth_handler.create_token({'sub': user_obj.username}, token_expires)
    return create_response(
        message='Login successful',
        obj=Token(
            access_token=token,
            expires_in=token_expires.seconds,
            user=UserSchema(**user_obj.model_dump())
        )
    )
