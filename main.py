import asyncio

import aiohttp
from aiohttp import web

from bot.webhooks import handle_bot_webhook, set_bot_webhook
from trello.boards import set_board
from trello.webhooks import (
    set_trello_webhook,
    handle_trello_webhook,
    accept_trello_webhook,
)
from database.models import setup_db
from settings.logger import logger
from settings import config


async def on_startup(_) -> None:
    """
    Performs setup tasks on bot startup.

    Sets up the database and sets the bot webhook.
    """
    await setup_db()
    await set_bot_webhook()


def setup_app() -> web.Application:
    """
    Sets up the web application.

    Creates routes for handling Telegram bot and Trello webhook requests.
    """
    app = web.Application()
    app.router.add_post(f"/{config.TELEGRAM_BOT_TOKEN}", handle_bot_webhook)
    app.router.add_head(f"/trello", accept_trello_webhook)
    app.router.add_post(f"/trello", handle_trello_webhook)
    app.on_startup.append(on_startup)

    return app


async def main() -> None:
    """
    Main entry point for the application.

    Sets up the web application, runs it, and sets up the Trello webhook.
    """
    app = setup_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    await site.start()

    async with aiohttp.ClientSession() as session:
        board_id = await set_board(session)
        await set_trello_webhook(session, board_id)


#
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("The bot was closed.")
    finally:
        loop.close()
