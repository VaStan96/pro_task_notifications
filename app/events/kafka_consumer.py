import json
from aiokafka import AIOKafkaConsumer

from db.session import get_db

from services.notifications_service import create_new_notification
import config

import logging

logger = logging.getLogger("kafka")

async def consume():
    # make Kafka-consumer
    logger.info("Make Kafka-Consumer")
    consumer = AIOKafkaConsumer(
        config.KAFKA_TOPIC_CREATE,
        config.KAFKA_TOPIC_DELETE,
        bootstrap_servers=config.KAFKA_SERVER,
        group_id=config.KAFKA_GROUP_ID_NOTIFICATION
    )
    
    # connect
    logger.info("Start Kafka-Consumer")
    await consumer.start()
    try:
        async for msg in consumer:
            # Decoding Kafka-message
            message = msg.value.decode('utf-8')
            task_data = json.loads(message)

            # make new Notification
            # Get the database session directly
            async for db in get_db(): # use async generator to get session
                logger.info("Request to make new notification")
                await create_new_notification(task_data, db) 
    finally:
        # disconnect
        logger.info("Stop Kafka-Consumer")
        await consumer.stop()
