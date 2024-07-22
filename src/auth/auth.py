import jwt

from argon2 import PasswordHasher
from typing import Annotated
from sqlmodel import select
from datetime import timedelta, datetime, timezone

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import settings
from src.models import User
from src.database import SessionDep


class AuthHandler:
    security_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
    ph = PasswordHasher()
    secret = settings.secret_key

    def hash_password(self, password):
        return self.ph.hash(password)

    def verify_password(self, hashed_password, plain_password):
        return self.ph.verify(hashed_password, plain_password)

    @staticmethod
    def create_token(data: dict, expires_in: timedelta):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_in
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm,
        )

    @staticmethod
    async def get_current_user(
            token: Annotated[str, Depends(security_scheme)],
            session: SessionDep,
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.exceptions.InvalidTokenError:
            raise credentials_exception
        user = await session.scalar(select(User).where(User.username == username))
        if user is None:
            raise credentials_exception
        return user
