from core.secrets_manager import SecretsManager


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

settings = Settings()
