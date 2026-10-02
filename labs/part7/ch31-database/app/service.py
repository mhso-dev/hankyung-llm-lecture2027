from __future__ import annotations

import asyncio

from sqlalchemy import select

from app.db import Session, engine
from app.models import Ticket


async def list_tickets() -> list[str]:
    """한 세션에서 상담 질문을 조회하고 연결을 즉시 반환합니다."""
    async with Session() as session:
        rows = await session.scalars(select(Ticket.question).order_by(Ticket.id))
        return list(rows)


async def main() -> None:
    print(await list_tickets())
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

