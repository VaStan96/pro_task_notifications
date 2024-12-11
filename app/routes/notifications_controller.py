from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from services import notifications_service
from schemas import RequestNotification, ResponseNotification
from db.session import get_db

router = APIRouter()

@router.get("/get", response_model=List[ResponseNotification])
async def get_notifications(db: AsyncSession = Depends(get_db)) -> List[ResponseNotification]:
    return await notifications_service.fetch_notifications(db)

@router.post("/create", response_model=ResponseNotification)
async def create_notification(request: RequestNotification, db: AsyncSession = Depends(get_db)) -> ResponseNotification:
    return await notifications_service.create_new_notification(request, db)

@router.put("/mark/{id}", response_model=ResponseNotification)
async def reading(id: int, db: AsyncSession = Depends(get_db)) -> ResponseNotification:
    return await notifications_service.reading(id, db)