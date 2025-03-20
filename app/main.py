# для запуска сервера:
# uvicorn main:app --reload
# библиотека имяФайла:переменнаяФастАпи --перезагрузка при сохранении

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from events import kafka_consumer
from events import scheduler

from logs import logging_config
from events import kafka_producer

from db import redis

from routes import notifications_controller


async def lifespan(app: FastAPI):
    # for logging
    producer = await kafka_producer.create_kafka_producer()
    logging_config.setup_logging_for_kafka(producer)
    # for Kafka-consumer
    loop = asyncio.get_event_loop()
    loop.create_task(kafka_consumer.consume())
    # auto notification (deadline check)
    await scheduler.start_scheduler()
    # cache
    await redis.get_redis()
    yield
    await producer.stop()
    await redis.close_redis()
 
app = FastAPI(
    title="Notification Service",
    description="Notification Service",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  # domens/ports
    allow_credentials=True,  # cookie and authorization
    allow_methods=["*"],  # all methods (GET, POST, PUT ...)
    allow_headers=["*"],  # headers in request
)

app.include_router(
    notifications_controller.router, # APIRouter-object
    prefix="/api/notifications", # Prefix for requests
    tags=["Notifications"] # Tags for http://localhost:8000/docs
)

