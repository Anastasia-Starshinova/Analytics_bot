import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") + WEBHOOK_PATH