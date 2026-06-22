import datetime

class KafkaProducerService:
    def __init__(self, producer):
        self.producer = producer

    async def send_to_kafka(self, topic: str, data: {}, event_name: str):

        message = self.build_events(event_name, data)
        await self.producer.send(topic=topic,value=message)
        await self.producer.flush()


    async def build_events(self, event_name: str, payload: dict):

        return {
            "event_name": event_name,
            "payload": payload,
            "created_at": datetime.datetime.now(),
            "source": "kafka-studio"
        }
