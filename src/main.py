from contextlib import asynccontextmanager
from src.config import settings
from src.database import init_db
from fastapi import FastAPI
from src.feed.router import router as main_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(main_router)
