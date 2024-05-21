from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from database.requests import set_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Handles the /start command sent by the user. This command is typically used
    to initialize the interaction with the bot.

    When a user sends the /start command, this function performs the following actions:
    1. Calls the `set_user` function to store the user's Telegram ID, username, and first name in the database.
    2. Sends a greeting message to the user, addressing them by their first name.

    Args:
        message (Message): The incoming message object containing details about the command and the user who sent it.

    Returns:
        None
    """
    await set_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        name=message.from_user.first_name,
    )
    await message.answer(f"Hello {message.from_user.first_name}!")
