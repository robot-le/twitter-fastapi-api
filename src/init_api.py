from fastapi import FastAPI
from src.main.router import router as main_router

app = FastAPI(
    title='Microblog',
)

app.include_router(main_router)
