from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import RequestNotification
from repositories import notifications_repository as repo
import utils

async def fetch_notifications(db: AsyncSession):
    db_notifications = await repo.get_all(db)

    if not db_notifications:
        raise HTTPException(status_code=404, detail="No notifications found")

    response_notifications = [utils.serilize_notification(notif) for notif in db_notifications]
    
    return response_notifications

async def fetch_notifications_by_user(db: AsyncSession, id: int):
    db_notifications = await repo.get_for_user(db, id)

    if not db_notifications:
        raise HTTPException(status_code=404, detail="No notifications found")

    response_notifications = [utils.serilize_notification(notif) for notif in db_notifications]
    
    return response_notifications


async def create_new_notification(new_request: dict, db: AsyncSession):
    complett_notification = utils.serilize_requestDict(new_request)
    
    request_notification = await repo.new(complett_notification, db)
    if request_notification is None:
        raise HTTPException(status_code=404, detail="Failed to create notification")
    
    response = utils.serilize_notification(request_notification)
    return response


async def reading (id: int, db: AsyncSession):
    notification = await repo.getByID(id, db)
    if not notification:
        raise HTTPException(status_code=404, detail="No notification with ID {id} found")
    
    notification.is_read = True
    readed_notification = await repo.saveChanges(notification, db)
    if not readed_notification:
        raise HTTPException(status_code=404, detail="Failed to mark notification")
    
    response = utils.serilize_notification(readed_notification)
    return response
    