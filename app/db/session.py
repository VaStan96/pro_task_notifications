from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import config

engine = create_async_engine(config.DB_URL, echo=True, future=True, pool_pre_ping=True)

local_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with local_session() as session:
        yield session