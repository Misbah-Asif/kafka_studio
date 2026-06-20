import logging
from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)
DEFAULT_CACHE_TTL_SECONDS = 900


@dataclass(frozen=True)
class CachedSecret:
    value: dict[str, Any]
    expires_at: float


class SecretsManager:
    def __init__(self, ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS):
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be greater than zero")

        self._ttl_seconds = ttl_seconds
        self._cache: dict[tuple[str, str], CachedSecret] = {}
        self._lock = RLock()

    def get_aws_secrets(self, region_name: str, secret_name: str) -> dict[str, Any]:
        cache_key = (region_name, secret_name)
        now = monotonic()

        with self._lock:
            cached_secret = self._cache.get(cache_key)
            if cached_secret and cached_secret.expires_at > now:
                return dict(cached_secret.value)

            try:
                client = boto3.client(
                    service_name="secretsmanager",
                    region_name=region_name,
                )
                response = client.get_secret_value(SecretId=secret_name)
            except (BotoCoreError, ClientError):
                logger.exception(
                    "Failed to fetch secret from AWS Secrets Manager: %s in %s",
                    secret_name,
                    region_name,
                )

                if cached_secret:
                    logger.warning(
                        "Using stale cached secret for %s in %s",
                        secret_name,
                        region_name,
                    )
                    return dict(cached_secret.value)

                return {}

            self._cache[cache_key] = CachedSecret(
                value=response,
                expires_at=monotonic() + self._ttl_seconds,
            )

            return dict(response)

    def clear_cache(self) -> None:
        with self._lock:
            self._cache.clear()


