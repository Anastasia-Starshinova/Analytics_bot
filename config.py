import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") + WEBHOOK_PATH

# WEBHOOK_PATH = f"/{TOKEN}"
# WEBHOOK_URL = f"https://familybudgetbot-production.up.railway.app{WEBHOOK_PATH}"