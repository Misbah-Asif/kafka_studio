import json

from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, result
from sqlalchemy import text


class Database:

    def __init__(self):
        self.session = None
        self.engine = None

    async def generate_pg_url(self, db_type: str):
        aws_secrets = settings.AWS_SECRETS
        if not aws_secrets:
            return None

        print("aws_secrets", aws_secrets)
        aws_secrets = json.loads(aws_secrets.get("SecretString", "")) if aws_secrets.get("SecretString", "") else {}
        db_host = aws_secrets["W_DB_HOST"] if db_type == "write" else aws_secrets["R_DB_HOST"]
        db_user = aws_secrets["W_DB_USER"] if db_type == "write" else aws_secrets["R_DB_USER"]
        db_password = aws_secrets["W_DB_PASSWORD"] if db_type == "write" else aws_secrets["R_DB_PASSWORD"]
        db_name = aws_secrets["W_DB_NAME"] if db_type == "write" else aws_secrets["R_DB_NAME"]
        db_port = aws_secrets["W_DB_PORT"] if db_type == "write" else aws_secrets["R_DB_PORT"]

        db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        return db_url


    async def create_db_engine(self, db_type: str):

        db_url = await self.generate_pg_url(db_type)
        print("database_url", db_url)

        if db_url:

            self.engine = create_async_engine(
                db_url,
                # todo: check for these values
                # pool_size=settings.DB_POOL_SIZE,
                # max_overflow=settings.DB_MAX_OVERFLOW,
                # pool_timeout=settings.DB_POOL_TIMEOUT,
                # pool_recycle=settings.DB_POOL_RECYCLE,

                # Health check stale connections
                pool_pre_ping=True,

                echo=False,
            )
            print("engine", self.engine)

    async def get_db(self, db_type: str = "read"):

        await self.create_db_engine(db_type=db_type)

        AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

    async def health_check(self, db_type: str = "read"):
        try:
            await self.create_db_engine(db_type=db_type)
            async with self.engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                value = result.scalar_one()
            return value
        except Exception as e:
            print("e", e)

db = Database()