from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import BigInteger, Column, Integer, String, Text, JSON, func, DateTime
from sqlalchemy.dialects.postgresql import INET, JSONB

class Base(DeclarativeBase):
    pass


class ConsumerMsgDump(Base):
    __tablename__ = "consumer_msg_dump"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_name = Column(String)
    event_data = Column(JSONB)
    consumer_started_at = Column(DateTime(timezone=True), server_default=func.now())
    consumer_ended_at = Column(DateTime(timezone=True), server_default=func.now())
    host = Column(Text)
    port = Column(Integer)
    ip_address = Column(INET)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
