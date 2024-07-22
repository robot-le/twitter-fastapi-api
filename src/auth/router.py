from typing import Annotated
from datetime import timedelta
from sqlmodel import select, or_

from src.config import settings
from src.models import UserInput, User, UserCreated, Token
from src.schemas import ResponseBase
from src.database import SessionDep
from src.auth.auth import AuthHandler

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/auth')
auth_handler = AuthHandler()


@router.post('/registration')
async def register(user: UserInput, session: SessionDep):
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

    hashed_pwd = auth_handler.hash_password(user.password1)
    u = User(
        username=user.username,
        email=user.email,
        password=hashed_pwd,
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)

    return JSONResponse(
        jsonable_encoder(ResponseBase[UserCreated](
            status='success',
            message='User successfully registered',
            data=UserCreated(**u.model_dump()),
        )),
        status_code=status.HTTP_201_CREATED,
        headers={'Location': 'url/to/user'}  # todo: change url
    )


@router.post('/login')
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep,
):
    user_obj = await session.scalar(select(User).where(User.username == form_data.username))
    if not user_obj or not auth_handler.verify_password(user_obj.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires = timedelta(minutes=settings.token_expire_time_minutes)
    token = auth_handler.create_token({'sub': user_obj.username}, token_expires)
    return JSONResponse(
        jsonable_encoder(ResponseBase[Token](
            status='success',
            message='Login successful',
            data=Token(
                access_token=token,
                token_type='Bearer',
                expires_in=token_expires.seconds,
                user=UserCreated(**user_obj.model_dump())
            )
        ))
    )


@router.get("/users/me/", response_model=UserCreated)
async def read_users_me(
        current_user: Annotated[User, Depends(auth_handler.get_current_user)],
):
    return UserCreated(**current_user.model_dump())
