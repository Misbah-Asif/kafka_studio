import logging

from sqlalchemy.ext.asyncio import AsyncSession
from repositories.consumer_msg_dump import ConsumerMsgRepository
from schemas.consumer_msg_dump import ConsumerMsgCreate

from core.config import settings


logger = logging.getLogger(__name__)


class ConsumerMsgService:
    def __init__(self, session: AsyncSession):
        try:
            self.repo = ConsumerMsgRepository(session=session)
        except Exception as e:
            logger.error(f"SERVICES : CONSUMER MSG DUMP : __init__ : Error : {e}")
            raise

    async def create_consumer_msg(self, payload: ConsumerMsgCreate):
        try:
            if payload.kafka:
                pass
            else:
                return await self.repo.create(
                    event_name=payload.event_name,
                    event_data=payload.event_data,
                )
        except Exception as e:
            logger.error(f"SERVICES : CONSUMER MSG DUMP : create_consumer_msg : Error : {e}")
            raise

