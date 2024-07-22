from fastapi.security import OAuth2PasswordBearer
from fastapi import Security
from src.config import settings
from argon2 import PasswordHasher


class AuthHandler:
    security_scheme = OAuth2PasswordBearer(tokenUrl='token')
    ph = PasswordHasher()
    secret = settings.secret_key

    def hash_password(self, password):
        return self.ph.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.ph.verify(hashed_password, plain_password)
