import logging

from sqlalchemy.ext.asyncio import AsyncSession
from models.consumer_msg_dump import ConsumerMsgDump

logger = logging.getLogger(__name__)


class ConsumerMsgRepository:
    def __init__(self, session: AsyncSession):
        try:
            self.session = session
        except Exception as e:
            logger.error(f"REPOSITORIES : CONSUMER MSG DUMP : __init__ : Error : {e}")
            raise

    async def create(self, event_name: str, event_data: dict):
        record = ConsumerMsgDump(event_name=event_name, event_data=event_data)
        try:
            self.session.add(record)
            await self.session.commit()
            await self.session.refresh(record)
            return record
        except Exception as e:
            logger.error(f"REPOSITORIES : CONSUMER MSG DUMP : create : Error : {e}")
            await self.session.rollback()
            raise
