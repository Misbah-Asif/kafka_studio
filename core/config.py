from core.secrets_manager import SecretsManager
from aiokafka import AIOKafkaProducer
import json

class Settings:
    def __init__(self):
        self.DEBUG = True

        self.AWS_REGION = "ap-south-1"
        self.AWS_SECRET_NAME = "kafka-studio/uat"
        self.DEFAULT_CACHE_TTL_SECONDS = 900

        secret_manager = SecretsManager(ttl_seconds=self.DEFAULT_CACHE_TTL_SECONDS)

        self.AWS_SECRETS: dict = secret_manager.get_aws_secrets(
            region_name=self.AWS_REGION, secret_name=self.AWS_SECRET_NAME
        )

        self.producer = AIOKafkaProducer(
            bootstrap_servers=["localhost:9092"],
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks="all",
            enable_idempotence=True,
            request_timeout_ms=40000
        )

settings = Settings()
