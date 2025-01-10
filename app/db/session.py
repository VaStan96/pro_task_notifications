from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql+asyncpg://admin:12345678@postgres:5432/ProTaskBD"

engine = create_async_engine(DB_URL, echo=True, future=True, pool_pre_ping=True)

local_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with local_session() as session:
        yield session