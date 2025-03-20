
import json
from aiokafka import AIOKafkaProducer
import config

class KafkaProducer:
    #Class-Wrapper
    def __init__(self, bootstrap_servers):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def send(self, message):
        await self.producer.send_and_wait(config.KAFKA_TOPIC_LOGS, json.dumps(message).encode("utf-8"))

    async def stop(self):
        await self.producer.stop()

# Make Kafka-Producer
async def create_kafka_producer():
    producer = KafkaProducer(config.KAFKA_SERVER)
    await producer.start()
    return producer
