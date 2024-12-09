import aiohttp

from settings import config
from settings.logger import logger
from trello.lists import create_lists


async def set_board(session: aiohttp.ClientSession) -> str:
    """
    Ensures the specified Trello board exists, creating it if necessary.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session to use for requests.

    Returns:
        str: The ID of the existing or newly created Trello board.
    """
    if board_id := await board_exists(session):
        logger.info(f"Board with name {config.BOARD_NAME} already exists.")
    else:
        board_id = await create_board(session)

    await create_lists(session, board_id)

    return board_id


async def create_board(session: aiohttp.ClientSession) -> str:
    """
    Creates a new Trello board.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session to use for requests.

    Returns:
        str: The ID of the newly created Trello board.

    Raises:
        RuntimeError: If the board creation fails.
    """
    board_data = {
        "key": config.TRELLO_API_KEY,
        "token": config.TRELLO_API_TOKEN,
        "name": config.BOARD_NAME,
        "defaultLists": "false",
    }
    async with session.post(
        config.TRELLO_API_CREATE_BOARD_URL, params=board_data
    ) as response:
        if response.status == 200:
            board = await response.json()
            logger.info("Board created successfully!")
            logger.info(f"Board ID: {board.get('id')}")
            return board.get("id")

        logger.error(f"Board wasn't created. Error status: {response.status}")
        logger.error(f"Error message: {await response.text()}")
        raise RuntimeError("Failed to create board")


async def board_exists(session: aiohttp.ClientSession) -> str | None:
    """
    Checks if the specified Trello board already exists.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session to use for requests.

    Returns:
        str | None: The ID of the existing board if found, otherwise None.
    """
    params = {"key": config.TRELLO_API_KEY, "token": config.TRELLO_API_TOKEN}
    async with session.get(
        config.TRELLO_API_GET_ALL_BOARDS_URL, params=params
    ) as response:
        if response.status == 200:
            boards_list = await response.json()
            for board in boards_list:
                if board.get("name") == config.BOARD_NAME:
                    return board.get("id")
        else:
            logger.error(
                f"List od boards wasn't received. Error status: {response.status}"
            )
            logger.error(f"Error message: {await response.text()}")

        return None
