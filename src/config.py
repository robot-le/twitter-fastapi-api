import os
from pydantic import EmailStr
from pydantic_settings import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    app_name: str = 'Microblog'
    secret_key: str
    database_uri: str = 'sqlite:///' + os.path.join(basedir, 'app.db')
    languages: list[str] = ['en', 'ru']
    token_expire_time_minutes: int = 30
    algorithm: str = 'HS256'
    post_char_limit: int = 140

    # mail_server: str | None
    # mail_port: int | None
    # mail_use_tls: bool
    # mail_username: str | None
    # mail_password: str | None
    # admins: list[EmailStr] | None


settings = Settings()
