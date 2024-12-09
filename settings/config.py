import os
from dotenv import load_dotenv

load_dotenv()

# Web Server
WEBHOOK = os.getenv("WEBHOOK")

# Telegram bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_URL = f"{WEBHOOK}/{TELEGRAM_BOT_TOKEN}"

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# Trello
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_CREATE_BOARD_URL = "https://api.trello.com/1/boards/"
TRELLO_API_GET_ALL_BOARDS_URL = "https://api.trello.com/1/members/me/boards"
TRELLO_API_CREATE_LIST_URL = "https://api.trello.com/1/lists"
TRELLO_API_WEBHOOK_URL = f"https://api.trello.com/1/webhooks"

BOARD_NAME = "Trello-Telegram-Board"
BOARD_LISTS = ["InProgress", "Done"]
TRELLO_WEBHOOK_URL = f"{WEBHOOK}/trello"
