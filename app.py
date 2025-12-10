from flask import Flask, request
import asyncio
from bot import bot, dp
import config

app = Flask(__name__)


# Запуск вебхука
@app.route(config.WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = request.json
    await dp.feed_webhook_update(bot, update)
    return "OK", 200


@app.before_request
def setup_webhook():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.set_webhook(config.WEBHOOK_URL))


@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"


if __name__ == "__main__":
    app.run(port=8080)