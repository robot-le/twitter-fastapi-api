from fastapi import FastAPI
from src.config import settings
from src.posts.router import router as posts_router
from src.users.router import router as users_router
from src.user.router import router as user_router
from src.auth.router import router as auth_router

app = FastAPI(
    title=settings.app_name,
)

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get('/check')
async def check():
    return {'ping': 'pong'}
