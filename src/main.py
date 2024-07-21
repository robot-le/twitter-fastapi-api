from src.config import settings
from fastapi import FastAPI
from src.posts.router import router as main_router


app = FastAPI(
    title=settings.app_name,
)

app.include_router(main_router)
