import aiohttp

from settings import config
from settings.logger import logger


async def create_lists(session: aiohttp.ClientSession, board_id: str) -> None:
    """
    Creates the necessary lists on the Trello board if they don't already exist.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session to use for requests.
        board_id (str): The ID of the Trello board.

    Raises:
        RuntimeError: If fetching the lists from the Trello board fails.
    """
    params = {
        "key": config.TRELLO_API_KEY,
        "token": config.TRELLO_API_TOKEN,
        "idBoard": board_id,
    }
    async with session.get(
        f"https://api.trello.com/1/boards/{board_id}/lists", params=params
    ) as response:
        if response.status == 200:
            existed_lists = [
                existed_list.get("name") for existed_list in await response.json()
            ]
            for list_name in config.BOARD_LISTS:
                if list_name in existed_lists:
                    logger.info(
                        f"Column with name '{list_name}' already exists on board."
                    )
                else:
                    await create_single_list(session, board_id, list_name)

        else:
            logger.error(
                f"Failed to fetch lists from Trello board. Error status: {response.status}"
            )
            raise RuntimeError("Failed to fetch lists from Trello board.")


async def create_single_list(
    session: aiohttp.ClientSession, board_id: str, list_name: str
) -> None:
    """
    Creates a single list on the Trello board.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session to use for requests.
        board_id (str): The ID of the Trello board.
        list_name (str): The name of the list to be created.

    Raises:
        RuntimeError: If the list creation fails.
    """
    list_data = {
        "key": config.TRELLO_API_KEY,
        "token": config.TRELLO_API_TOKEN,
        "name": list_name,
        "idBoard": board_id,
    }
    async with session.post(
        config.TRELLO_API_CREATE_LIST_URL, params=list_data
    ) as response:
        if response.status == 200:
            list_info = await response.json()
            logger.info(f"List '{list_name}' created successfully!")
            logger.info(f"List ID: {list_info.get('id')}")
        else:
            logger.error(
                f"List '{list_name}' wasn't created. Error status: {response.status}"
            )
            logger.error(f"Error message: {await response.text()}")
            raise RuntimeError("Failed to create list")
