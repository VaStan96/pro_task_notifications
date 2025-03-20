import logging
# from logging.handlers import KafkaLoggingHandler
from logs.kafka_handler import KafkaLogHandler
import config

def setup_logging_for_kafka(producer):
    
    kafka_handler = KafkaLogHandler(producer)
    
    kafka_logger = logging.getLogger("kafka")
    kafka_logger.setLevel(logging.INFO)
    kafka_logger.addHandler(kafka_handler)
    
    return kafka_logger