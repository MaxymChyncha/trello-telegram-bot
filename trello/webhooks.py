import os

from aiohttp import web, ClientResponse, ClientSession
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from bot.webhooks import bot
from settings import config
from settings.logger import logger


async def set_trello_webhook(session: ClientSession, board_id: str) -> ClientResponse:
    """
    Sets up a webhook for Trello board updates.

    Args:
        session (ClientSession): The aiohttp client session to use for requests.
        board_id (str): The ID of the Trello board.

    Returns:
        ClientResponse: The HTTP response from setting up the webhook.
    """
    async with session.post(
        config.TRELLO_API_WEBHOOK_URL,
        params={
            "key": config.TRELLO_API_KEY,
            "idModel": board_id,
            "callbackURL": config.TRELLO_WEBHOOK_URL,
            "token": config.TRELLO_API_TOKEN,
            "description": "Webhook",
        },
    ) as response:
        response_text = await response.text()

        if response.status != 200:
            logger.error(f"Failed to create webhook: {response_text}")
        else:
            logger.info("Trello webhook was created")
        return response


async def accept_trello_webhook(request: Request) -> Response:
    """
    Handles the initial validation request from Trello webhook.

    Args:
        request (Request): The incoming HTTP request from Trello.

    Returns:
        Response: HTTP 200 response indicating successful validation.
    """
    logger.info("Trello webhook validation request was received")
    return web.Response(status=200)


async def handle_trello_webhook(request: Request):
    """
    Handles incoming webhook events from Trello.

    Args:
        request (Request): The incoming HTTP request from Trello.

    Returns:
        Response: HTTP 200 response indicating successful handling of the webhook.
    """
    data = await request.json()
    logger.debug(f"Data: {data}")

    if data.get("action", {}).get("type") == "updateCard":
        card = data["action"]["data"]["card"]["name"]
        old_list = data["action"]["data"]["listBefore"]["name"]
        new_list = data["action"]["data"]["listAfter"]["name"]
        board = data["action"]["data"]["board"]["name"]
        member = data["action"]["memberCreator"]["fullName"]

        message = (
            f"Card '{card}' was moved from list '{old_list}' "
            f"to list '{new_list}' on board '{board}' by {member}"
        )
        await bot.send_message(chat_id=os.getenv("TELEGRAM_GROUP_ID"), text=message)

    return web.Response(status=200)
