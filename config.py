import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") + WEBHOOK_PATH
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
