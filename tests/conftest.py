import os
import asyncio
from typing import AsyncGenerator, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest
from src.main import app
from src.database import get_session
from httpx import AsyncClient
from sqlalchemy.pool import NullPool

engine_test = create_async_engine(
    os.environ.get('TEST_DATABASE_URI'),
    poolclass=NullPool,
)

async_session_maker = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_async_session():
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def access_data(ac) -> list[dict[str, Any]]:

    access_data_lst = []

    try:
        for i in range(3):

            await ac.post(
                app.url_path_for('register'),
                json={
                    'username': f'test_username_{i}',
                    'email': f'test_{i}@mail.com',
                    'password': 'password',
                    'password2': 'password',
                }
            )

            login_res = await ac.post(
                app.url_path_for('login'),
                data={
                    'username': f'test_username_{i}',
                    'password': 'password',
                }
            )
            data = login_res.json()
            a_token = data.get('obj', {}).get('access_token')
            user_id = data.get('obj', {}).get('user', {}).get('id')
            access_data_lst.append({'user_token': a_token, 'user_id': user_id})
    except Exception as e:
        pytest.exit(f'Exception from token fixture was thrown: {str(e)}')

    return access_data_lst
