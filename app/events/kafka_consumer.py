import json
from aiokafka import AIOKafkaConsumer

from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
#from fastapi import Depends

from services.notifications_service import create_new_notification
import config

async def consume():
    # make Kafka-consumer
    consumer = AIOKafkaConsumer(
        config.KAFKA_TOPIC,
        bootstrap_servers=config.KAFKA_SERVER,
        group_id=config.KAFKA_GROUP_ID
    )
    
    # connect
    await consumer.start()
    try:
        async for msg in consumer:
            # Decoding Kafka-message
            message = msg.value.decode('utf-8')
            task_data = json.loads(message)

            # make new Notification
            # Get the database session directly
            async for db in get_db(): # use async generator to get session
                await create_new_notification(task_data, db) 
    finally:
        # disconnect
        await consumer.stop()


# async def create_notification(request: dict, db: AsyncSession):
#     return await create_new_notification(request, db)