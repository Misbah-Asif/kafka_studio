import logging
from fastapi import Depends, APIRouter
from dependencies.database import db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.consumer_msg_dump import ConsumerMsgCreate, ConsumerMsgResponse
from services.consumer_msg_dump import ConsumerMsgService

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/consumer-msg",
    tags=["Consumer Messages"],
)

async def get_write_db():
    try:
        async for session in db.get_db(db_type="write"):
            yield session
    except Exception as e:
        logger.error(f"ENDPOINTS : CONSUMER MSG DUMP : get_write_db : Error : {e}")
        raise


async def get_read_db():
    try:
        async for session in db.get_db(db_type="read"):
            yield session
    except Exception as e:
        logger.error(f"ENDPOINTS : CONSUMER MSG DUMP : get_read_db : Error : {e}")
        raise


@router.post("/", response_model=ConsumerMsgResponse)
async def create_consumer_msg(consumer_msg: ConsumerMsgCreate, session: AsyncSession = Depends(get_write_db)):
    try:
        service = ConsumerMsgService(session)
        return await service.create_consumer_msg(payload=consumer_msg)
    except Exception as e:
        logger.error(f"ENDPOINTS : CONSUMER MSG DUMP : create_consumer_msg : Error : {e}")
        raise
