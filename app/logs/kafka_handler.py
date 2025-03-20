import datetime
import logging
import asyncio
from events import kafka_producer
import json

class KafkaLogHandler(logging.Handler):

    def __init__(self, producer):
        super().__init__()
        self.producer = producer

    async def emit_async(self, record):
        log_entry = {
            "@timestamp": datetime.datetime.fromtimestamp(record.created, datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "service": "Notification-Service",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.module,
            "funcName": record.funcName if record.funcName else "unknown",
        }
        await self.producer.send(log_entry)

    def emit(self, record):
        asyncio.create_task(self.emit_async(record))
