from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, select
from sqlalchemy.orm import selectinload

from models import Task

async def get_all(db: AsyncSession):
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.notifications), selectinload(Task.user))
        .order_by(asc(Task.id))
    )
    db_tasks = result.scalars().all()  # get list of objects Task
    return  db_tasks

async def get_tasks_with_deadline(db: AsyncSession, deadline: datetime):
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.notifications), selectinload(Task.user))
        .where(Task.deadline <= deadline)
        .order_by(asc(Task.id))
    )
    db_tasks = result.scalars().all()  # get list of objects Task
    return  db_tasks