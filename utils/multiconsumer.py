import json
import asyncio
import logging

from aiokafka import AIOKafkaConsumer
from core.config import settings

logger = logging.getLogger(__name__)


def json_deserializer(value):
    if value is None:
        return None
    return json.loads(value.decode("utf-8"))


class KafkaMultiConsumerService:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            client_id='kafka-studio-consumer-client',
            group_id='kafka-studio-consumer-group',
            key_deserializer=json_deserializer,
            value_deserializer=json_deserializer,
            enable_auto_commit=False,
            auto_offset_reset="latest"
        )
        self._started = False

    async def start(self):
        self.consumer.subscribe(topics=settings.kafka_topics)
        try:
            await self.consumer.start()
        except Exception:
            logger.exception(
                "Failed to start Kafka consumer with bootstrap servers: %s",
                settings.kafka_bootstrap_servers,
            )
            await self.stop()
            raise
        self._started = True

    async def stop(self):
        if self.consumer is None:
            return
        await self.consumer.stop()
        self._started = False

    async def consume(self):
        async for message in self.consumer:
            event_data = message.value
            event_topic = message.topic
            print("event_data", event_data)
            print("event_topic", event_topic)
            await self.consumer.commit()


async def main():
    service = KafkaMultiConsumerService()
    try:
        await service.start()
        await service.consume()
    finally:
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())
