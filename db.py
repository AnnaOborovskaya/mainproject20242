from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models.courier_users import *
from models.orders_model import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

ur_a = settings.POSTGRES_DATABASE_URLA

engine_s = create_async_engine(ur_a, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(engine_s, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with engine_s.begin() as conn:
        pass
