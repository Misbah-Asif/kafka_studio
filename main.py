from logging import shutdown

import uvicorn
from fastapi import FastAPI
from dependencies.database import db
from api.v1.endpoints.consumer_msg_dump import router as consumer_msg_router

app = FastAPI(
title="Kafka Studio API",
    version="1.0.0",
)

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

logger.info("Application started")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/db-health")
async def db_health():
    r_ping_status = await db.health_check(db_type="read")
    w_ping_status = await db.health_check(db_type="write")
    return {"r_db_status": r_ping_status, "w_db_status": w_ping_status}

app.include_router(
    consumer_msg_router,
    prefix="/api/v1",
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
