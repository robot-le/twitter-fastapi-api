from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User


from src.database import get_session
SessionDep = Annotated[AsyncSession, Depends(get_session)]

from src.auth.auth import AuthHandler
auth_handler = AuthHandler()
CurrentUserDep = Annotated[User, Depends(auth_handler.get_current_user)]
AuthDep = Annotated[User, Depends(auth_handler.auth)]
