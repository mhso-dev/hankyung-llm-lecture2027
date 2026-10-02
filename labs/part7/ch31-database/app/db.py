from __future__ import annotations

import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "CH31_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:55431/ch31_lab",
)
engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=5, pool_timeout=5)
Session = async_sessionmaker(engine, expire_on_commit=False)


async def session_scope() -> AsyncSession:
    """요청 하나에서 사용할 새 세션을 반환합니다."""
    return Session()

