from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.session import get_db
from services.notifications_service import check_deadline

async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=check_notifications_task,
        trigger="interval",
        hours=1,
    )
    scheduler.start()

async def check_notifications_task():
    async for db in get_db(): # use async generator to get session
        await check_deadline(db)