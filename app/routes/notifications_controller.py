import logging
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services import notifications_service
from schemas import RequestNotification, ResponseNotification
from db.session import get_db
import security

router = APIRouter()
logger = logging.getLogger("kafka")

@router.get("/", response_model=List[ResponseNotification])
async def get_notifications(db: AsyncSession = Depends(get_db)) -> List[ResponseNotification]:
    logger.info("Request to receive all notifications")
    return await notifications_service.fetch_notifications(db)

@router.get("/getByUser", response_model=List[ResponseNotification])
async def get_notifications_by_user(db: AsyncSession = Depends(get_db), current_user: dict = Depends(security.get_current_user)) -> List[ResponseNotification]:
    logger.info("Request to receive all notifications for an authorized user")
    return await notifications_service.fetch_notifications_by_user(db, int(current_user["sub"]))

# @router.post("/create", response_model=ResponseNotification)
# async def create_notification(request: RequestNotification, db: AsyncSession = Depends(get_db)) -> ResponseNotification:
#     return await notifications_service.create_new_notification(request, db)

@router.put("/mark/{id}", response_model=ResponseNotification)
async def reading(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(security.get_current_user)) -> ResponseNotification:
    logger.info(f"Request to change status for notification with ID-{id}")
    return await notifications_service.reading(id, db)