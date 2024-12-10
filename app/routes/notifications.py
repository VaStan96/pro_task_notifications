from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import Notification
from schemas import ResponseNotification
from db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[ResponseNotification])
async def get_notifications(db: AsyncSession = Depends(get_db)) -> List[ResponseNotification]:
    result = await db.execute(select(Notification).options(selectinload(Notification.task), selectinload(Notification.user)))
    db_notifications = result.scalars().all()  # Получаем список объектов Notification
    return [
        ResponseNotification(
            id=notif.id,
            message=notif.message,
            task_name=notif.task.name,
            user_name=notif.user.name,
            created_at=notif.created_at,
            is_read=notif.is_read
        )
        for notif in db_notifications
    ]

# @router.post("/", Resporesponse_model=Notification)
# async def create_notification(notification: NewNotification, ) -> Notification:
#     db = Depends()
#     return {"message": "Notification created", "data": notification}