from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models import Notification

async def get_all(db: AsyncSession):
    result = await db.execute(select(Notification).options(selectinload(Notification.task), selectinload(Notification.user)))
    db_notifications = result.scalars().all()  # get list of objects Notification
    return  db_notifications


async def new(newNotification: Notification, db: AsyncSession):
    db.add(newNotification)
    await db.commit()
    await db.refresh(newNotification)

    result = await db.execute(
        select(Notification)
        .options(selectinload(Notification.task), selectinload(Notification.user))
        .where(Notification.id == newNotification.id)
    )
    notification = result.scalar_one_or_none()

    return notification
    

async def getByID(id: int, db: AsyncSession):
    sql_request = select(Notification).where(Notification.id == id)
    notification = await db.execute(sql_request)
    return notification.scalar_one_or_none()


async def saveChanges(notification: Notification, db: AsyncSession):
    await db.commit()
    await db.refresh(notification)
    result = await db.execute(
        select(Notification)
        .options(selectinload(Notification.task), selectinload(Notification.user))
        .where(Notification.id == notification.id)
    )
    notification = result.scalar_one_or_none()
    
    return notification
    
