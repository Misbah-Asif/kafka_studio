import datetime
from aiokafka import AIOKafkaProducer
import json

class KafkaProducerService:
    def __init__(self):

        self.producer = AIOKafkaProducer(
            bootstrap_servers=["localhost:9092"],
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
            acks="all",
            enable_idempotence=True,
            request_timeout_ms=40000
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        if self.producer is not None:
            await self.producer.stop()
            self.producer = None

    async def send_to_kafka(self, topic: str, data: dict, event_name: str):
        message = await self.build_events(event_name, data)
        await self.producer.send(topic=topic,value=message)
        await self.producer.flush()

    async def build_events(self, event_name: str, payload: dict):

        return {
            "event_name": event_name,
            "payload": payload,
            "created_at": datetime.datetime.now(),
            "source": "kafka-studio"
        }

kps = KafkaProducerService()
