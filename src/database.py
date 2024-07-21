from sqlmodel import create_engine, SQLModel, Session
from src.config import settings

engine = create_engine(
    settings.database_uri,
    echo=True,
)


def init_db():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
