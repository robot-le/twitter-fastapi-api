from fastapi import APIRouter, HTTPException
from src.models import UserInput, User, UserCreated
from src.auth.auth import AuthHandler
from src.database import SessionDep
from sqlmodel import select, or_
from fastapi import status
from fastapi.responses import JSONResponse
from src.schemas import ResponseBase
from fastapi.encoders import jsonable_encoder

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
            status_code=400,
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
async def login():
    pass
