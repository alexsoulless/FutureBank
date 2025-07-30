from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.config import DB_PASSWORD, DB_USER, DB_HOST, DB_NAME, DB_PORT

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def test_db_connection():
    try:
        async for session in get_session():
            result = await session.execute(text("SELECT * from users;"))
    except Exception as ex:
        raise Exception(f"Failed to connect DB:\n{ex.__repr__()}")