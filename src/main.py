from src.config import settings
from fastapi import FastAPI
from src.posts.router import router as posts_router
from src.auth.router import router as auth_router


app = FastAPI(
    title=settings.app_name,
)


app.include_router(posts_router)
app.include_router(auth_router)
