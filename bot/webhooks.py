from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from bot.handlers import router
from settings import config
from settings.logger import logger

bot = Bot(
    token=config.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
dp.include_router(router)


async def set_bot_webhook() -> None:
    """
    Sets the Telegram bot webhook.

    Attempts to set the bot's webhook URL from the configuration.
    Logs success or error messages based on the outcome.
    """
    try:
        await bot.set_webhook(config.TELEGRAM_WEBHOOK_URL)
        logger.info("Bot webhook was created")
    except Exception as err:
        logger.error(f"Failed to set bot webhook: {err}")


async def handle_bot_webhook(request: Request) -> Response:
    """
    Handles incoming Telegram bot webhook requests.

    Processes JSON POST requests, validates the token, and feeds the update
    to the dispatcher. Returns a 200 status for valid requests, otherwise 403.

    Args:
        request (Request): Incoming HTTP request with update data.

    Returns:
        Response: HTTP 200 on success, 403 on failure.
    """
    if request.content_type == "application/json":
        data = await request.json()
        token = request.path.split("/")[-1]

        if token == config.TELEGRAM_BOT_TOKEN:
            update = types.Update(**data)
            await dp.feed_update(bot, update)
            return web.Response(status=200)

    return web.Response(status=403)
