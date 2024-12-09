from database.models import async_session
from database.models import TGUser
from sqlalchemy import select


async def set_user(tg_id: int, name: str, username: str) -> None:
    """
    Adds a new user to the database if not already present.

    Args:
        tg_id (int): Telegram user ID.
        name (str): User's name.
        username (str): User's username.
    """
    async with async_session() as session:
        user = await session.scalar(select(TGUser).where(TGUser.tg_id == tg_id))

        if not user:
            session.add(TGUser(tg_id=tg_id, name=name, username=username))
            await session.commit()
