from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.session import get_db
from services.notifications_service import check_deadline

import logging

logger = logging.getLogger("kafka")

async def start_scheduler():
    logger.info("Make Scheduler")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=check_notifications_task,
        trigger="interval",
        hours=1,
    )
    logger.info("Start Scheduler")
    scheduler.start()

async def check_notifications_task():
    async for db in get_db(): # use async generator to get session
        logger.info("Request to check deadlines")
        await check_deadline(db)