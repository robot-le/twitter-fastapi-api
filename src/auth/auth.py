import jwt

from argon2 import PasswordHasher
from typing import Annotated
from sqlmodel import select
from datetime import timedelta, datetime, timezone

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import settings
from src.models import User
from src.dependencies import SessionDep


class AuthHandler:
    security_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
    ph = PasswordHasher()
    secret = settings.secret_key

    def hash_password(self, password):
        return self.ph.hash(password)

    def verify_password(self, hashed_password, plain_password):
        return self.ph.verify(hashed_password, plain_password)

    @staticmethod
    def create_token(data: dict, expires_in: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_in
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm,
        )

    async def get_current_user(
            self,
            token: Annotated[str, Depends(security_scheme)],
            session: SessionDep,
    ) -> User:
        payload = self.decode_token(token)
        username: str = payload.get('sub')
        user = await session.scalar(select(User).where(User.username == username))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return user

    def auth(self, token: Annotated[str, Depends(security_scheme)]) -> dict:
        return self.decode_token(token)

    @staticmethod
    def decode_token(token) -> dict:
        try:
            return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        except jwt.ExpiredSignatureError:
            error = 'Expired signature'
        except jwt.InvalidTokenError:
            error = 'Invalid token'

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={'WWW-Authenticate': 'Bearer'},
        )
