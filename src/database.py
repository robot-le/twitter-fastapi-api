from sqlmodel import create_engine, SQLModel, Session
from src.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    settings.database_uri,
    echo=True,
    future=True,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


# async def get_session():
#     session = AsyncSession(engine)
#     try:
#         yield session
#     finally:
#         await session.close()

async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
