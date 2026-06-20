import uvicorn
from fastapi import FastAPI
from dependencies.database import db

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/db-health")
async def db_health():
    r_ping_status = await db.health_check(db_type="read")
    w_ping_status = await db.health_check(db_type="write")
    return {"r_db_status": r_ping_status, "w_db_status": w_ping_status}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
