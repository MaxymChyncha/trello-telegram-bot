from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from settings import config

engine = create_async_engine(url=config.DATABASE_URL)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TGUser(Base):
    __tablename__ = "tg_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(63))
    name: Mapped[str] = mapped_column(String(63))


async def setup_db() -> None:
    """
    Sets up the database.

    Creates all database tables using SQLAlchemy's metadata.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
